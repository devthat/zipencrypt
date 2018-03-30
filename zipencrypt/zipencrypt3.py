import os
import stat
from zipfile import ZipFile as BaseZipfile, ZipInfo, ZIP_STORED, ZIP64_LIMIT, \
    ZIP_DEFLATED, LargeZipFile, crc32, \
    _ZipDecrypter, ZIP_LZMA, _get_compressor

import struct

import time

# randomFunc = os.urandom
randomFunc = lambda n: b"X"*n


class _ZipEncrypter(_ZipDecrypter):
    def __call__(self, c):
        """Decrypt a single character."""
        assert isinstance(c, int)
        k = self.key2 | 2
        _c = c ^ (((k * (k^1)) >> 8) & 255)
        self._UpdateKeys(c)
        return _c


class ZipFile(BaseZipfile):
    def write(self, filename, arcname=None, compress_type=None, pwd=None):
        """Put the bytes from filename into the archive under the name
        arcname."""
        if not self.fp:
            raise RuntimeError(
                "Attempt to write to ZIP archive that was already closed")
        if pwd and not isinstance(pwd, bytes):
            raise TypeError("pwd: expected bytes, got %s" % type(pwd))

        st = os.stat(filename)
        isdir = stat.S_ISDIR(st.st_mode)
        mtime = time.localtime(st.st_mtime)
        date_time = mtime[0:6]
        # Create ZipInfo instance to store file information
        if arcname is None:
            arcname = filename
        arcname = os.path.normpath(os.path.splitdrive(arcname)[1])
        while arcname[0] in (os.sep, os.altsep):
            arcname = arcname[1:]
        if isdir:
            arcname += '/'
        zinfo = ZipInfo(arcname, date_time)
        zinfo.external_attr = (st[0] & 0xFFFF) << 16      # Unix attributes
        if isdir:
            zinfo.compress_type = ZIP_STORED
        elif compress_type is None:
            zinfo.compress_type = self.compression
        else:
            zinfo.compress_type = compress_type

        zinfo.file_size = st.st_size
        zinfo.flag_bits = 0x00
        with self._lock:
            if self._seekable:
                self.fp.seek(self.start_dir)
            zinfo.header_offset = self.fp.tell()    # Start of header bytes
            if zinfo.compress_type == ZIP_LZMA:
                # Compressed data includes an end-of-stream (EOS) marker
                zinfo.flag_bits |= 0x02

            self._writecheck(zinfo)
            self._didModify = True

            if isdir:
                zinfo.file_size = 0
                zinfo.compress_size = 0
                zinfo.CRC = 0
                zinfo.external_attr |= 0x10  # MS-DOS directory flag
                self.filelist.append(zinfo)
                self.NameToInfo[zinfo.filename] = zinfo
                self.fp.write(zinfo.FileHeader(False))
                self.start_dir = self.fp.tell()
                return

            cmpr = _get_compressor(zinfo.compress_type)
            if not self._seekable:
                zinfo.flag_bits |= 0x08
            pwd = pwd or self.pwd
            if pwd:
                zinfo.flag_bits |= 0x8 | 0x1  # set stream and encrypted
            with open(filename, "rb") as fp:
                # Must overwrite CRC and sizes with correct data later
                zinfo.CRC = CRC = 0
                zinfo.compress_size = compress_size = 0
                # Compressed size can be larger than uncompressed size
                zip64 = self._allowZip64 and \
                    zinfo.file_size * 1.05 > ZIP64_LIMIT
                self.fp.write(zinfo.FileHeader(zip64))
                pwd = pwd or self.pwd
                if pwd:
                    ze = _ZipEncrypter(pwd)
                    encrypt = lambda x: bytes(map(ze, x))
                    zinfo._raw_time = (
                        zinfo.date_time[3] << 11
                        | zinfo.date_time[4] << 5
                        | (zinfo.date_time[5] // 2))
                    check_byte = (zinfo._raw_time >> 8) & 0xff
                    encryption_header = randomFunc(11) + struct.pack("B",
                                                                    check_byte)
                    self.fp.write(encrypt(encryption_header))
                else:
                    encrypt = lambda x: x
                file_size = 0
                while 1:
                    buf = fp.read(1024 * 8)
                    if not buf:
                        break
                    file_size = file_size + len(buf)
                    CRC = crc32(buf, CRC)
                    if cmpr:
                        buf = cmpr.compress(buf)
                        compress_size = compress_size + len(buf)
                    self.fp.write(encrypt(buf))
            if cmpr:
                buf = cmpr.flush()
                compress_size = compress_size + len(buf)
                self.fp.write(encrypt(buf))
                zinfo.compress_size = compress_size
            else:
                zinfo.compress_size = file_size
            zinfo.CRC = CRC
            zinfo.file_size = file_size
            if zinfo.flag_bits & 0x08:
                # Write CRC and file sizes after the file data
                if pwd:
                    zinfo.compress_size += 12
                fmt = '<LQQ' if zip64 else '<LLL'
                self.fp.write(struct.pack(fmt, zinfo.CRC, zinfo.compress_size,
                                          zinfo.file_size))
                self.start_dir = self.fp.tell()
            else:
                if not zip64 and self._allowZip64:
                    if file_size > ZIP64_LIMIT:
                        raise RuntimeError('File size has increased during compressing')
                    if compress_size > ZIP64_LIMIT:
                        raise RuntimeError('Compressed size larger than uncompressed size')
                # Seek backwards and write file header (which will now include
                # correct CRC and file sizes)
                self.start_dir = self.fp.tell() # Preserve current position in file
                self.fp.seek(zinfo.header_offset)
                self.fp.write(zinfo.FileHeader(zip64))
                self.fp.seek(self.start_dir)
            self.filelist.append(zinfo)
            self.NameToInfo[zinfo.filename] = zinfo

    def writestr(self, zinfo_or_arcname, data, compress_type=None, pwd=None):
        """Write a file into the archive.  The contents is 'data', which
        may be either a 'str' or a 'bytes' instance; if it is a 'str',
        it is encoded as UTF-8 first.
        'zinfo_or_arcname' is either a ZipInfo instance or
        the name of the file in the archive."""
        if isinstance(data, str):
            data = data.encode("utf-8")
        if not isinstance(zinfo_or_arcname, ZipInfo):
            zinfo = ZipInfo(filename=zinfo_or_arcname,
                            date_time=time.localtime(time.time())[:6])
            zinfo.compress_type = self.compression
            if zinfo.filename[-1] == '/':
                zinfo.external_attr = 0o40775 << 16   # drwxrwxr-x
                zinfo.external_attr |= 0x10           # MS-DOS directory flag
            else:
                zinfo.external_attr = 0o600 << 16     # ?rw-------
        else:
            zinfo = zinfo_or_arcname

        if not self.fp:
            raise RuntimeError(
                "Attempt to write to ZIP archive that was already closed")

        if pwd and not isinstance(pwd, bytes):
            raise TypeError("pwd: expected bytes, got %s" % type(pwd))

        zinfo.file_size = len(data)            # Uncompressed size
        with self._lock:
            if self._seekable:
                self.fp.seek(self.start_dir)
            zinfo.header_offset = self.fp.tell()    # Start of header data
            if compress_type is not None:
                zinfo.compress_type = compress_type
            zinfo.header_offset = self.fp.tell()    # Start of header data
            if compress_type is not None:
                zinfo.compress_type = compress_type
            if zinfo.compress_type == ZIP_LZMA:
                # Compressed data includes an end-of-stream (EOS) marker
                zinfo.flag_bits |= 0x02

            self._writecheck(zinfo)
            self._didModify = True
            zinfo.CRC = crc32(data)       # CRC-32 checksum
            co = _get_compressor(zinfo.compress_type)
            if co:
                data = co.compress(data) + co.flush()
                zinfo.compress_size = len(data)    # Compressed size
            else:
                zinfo.compress_size = zinfo.file_size
            zip64 = zinfo.file_size > ZIP64_LIMIT or \
                zinfo.compress_size > ZIP64_LIMIT
            if zip64 and not self._allowZip64:
                raise LargeZipFile("Filesize would require ZIP64 extensions")

            pwd = pwd or self.pwd
            if pwd:
                zinfo.flag_bits |= 0x01
                zinfo.compress_size += 12  # 12 extra bytes for the header
                if zinfo.flag_bits & 0x8:
                    zinfo._raw_time = (
                        zinfo.date_time[3] << 11
                        | zinfo.date_time[4] << 5
                        | (zinfo.date_time[5] // 2))
                    check_byte = (zinfo._raw_time >> 8) & 0xff
                else:
                    check_byte = (zinfo.CRC >> 24) & 0xff
                encryption_header = randomFunc(11) + struct.pack("B", check_byte)
                ze = _ZipEncrypter(pwd)
                data = bytes(map(ze, encryption_header + data))

            self.fp.write(zinfo.FileHeader(zip64))
            self.fp.write(data)
            if zinfo.flag_bits & 0x08:
                # Write CRC and file sizes after the file data
                fmt = '<LQQ' if zip64 else '<LLL'
                self.fp.write(struct.pack(fmt, zinfo.CRC, zinfo.compress_size,
                                          zinfo.file_size))
            self.fp.flush()
            self.start_dir = self.fp.tell()
            self.filelist.append(zinfo)
            self.NameToInfo[zinfo.filename] = zinfo
