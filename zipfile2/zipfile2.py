import os
import stat
import struct
import time
import zlib
from zipfile import ZipFile as BaseZipfile, ZipInfo, ZIP_STORED, ZIP64_LIMIT, \
    ZIP_DEFLATED, LargeZipFile, crc32, \
    _ZipDecrypter

randomFunc = os.urandom


class _ZipEncrypter(_ZipDecrypter):
    def __call__(self, c):
        """Encrypt a single character."""
        _c = ord(c)
        k = self.key2 | 2
        _c = _c ^ (((k * (k ^ 1)) >> 8) & 255)
        _c = chr(_c)
        self._UpdateKeys(c)  # this is the only line that actually changed
        return _c


class ZipFile(BaseZipfile):
    def write(self, filename, arcname=None, compress_type=None, pwd=None):
        """Put the bytes from filename into the archive under the name
        arcname."""
        if not self.fp:
            raise RuntimeError(
                "Attempt to write to ZIP archive that was already closed")

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
        zinfo.external_attr = (st[0] & 0xFFFF) << 16L  # Unix attributes
        if isdir:
            zinfo.compress_type = ZIP_STORED
        elif compress_type is None:
            zinfo.compress_type = self.compression
        else:
            zinfo.compress_type = compress_type

        zinfo.file_size = st.st_size
        zinfo.flag_bits = 0x00
        zinfo.header_offset = self.fp.tell()  # Start of header bytes

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
            return

        with open(filename, "rb") as fp:
            # Must overwrite CRC and sizes with correct data later
            zinfo.CRC = CRC = 0
            zinfo.compress_size = compress_size = 0
            # Compressed size can be larger than uncompressed size
            zip64 = self._allowZip64 and \
                    zinfo.file_size * 1.05 > ZIP64_LIMIT
            self.fp.write(zinfo.FileHeader(zip64))
            if zinfo.compress_type == ZIP_DEFLATED:
                cmpr = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION,
                                        zlib.DEFLATED, -15)
            else:
                cmpr = None
            pwd = pwd or self.pwd
            if pwd:
                zinfo.flag_bits |= 0x8 | 0x1  # set stream and encrypted
                ze = _ZipEncrypter(pwd)
                encrypt = lambda x: "".join(map(ze, x))
                zinfo._raw_time = (
                    zinfo.date_time[3] << 11
                    | zinfo.date_time[4] << 5
                    | (zinfo.date_time[5] // 2))
                check_byte = (zinfo._raw_time >> 8) & 0xff
                enryption_header = randomFunc(11) + chr(check_byte)
                self.fp.write(encrypt(enryption_header))
            else:
                encrypt = lambda x: x
            file_size = 0
            while 1:
                buf = fp.read(1024 * 8)
                if not buf:
                    break
                file_size = file_size + len(buf)
                CRC = crc32(buf, CRC) & 0xffffffff
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
        if not zip64 and self._allowZip64:
            if file_size > ZIP64_LIMIT:
                raise RuntimeError(
                    'File size has increased during compressing')
            if compress_size > ZIP64_LIMIT:
                raise RuntimeError(
                    'Compressed size larger than uncompressed size')
        if pwd:
            # Write CRC and file sizes after the file data
            zinfo.compress_size += 12
            fmt = '<LQQ' if zip64 else '<LLL'
            self.fp.write(struct.pack(
                fmt, zinfo.CRC, zinfo.compress_size, zinfo.file_size))
            self.fp.flush()
        else:
            # Seek backwards and write file header (which will now include
            # correct CRC and file sizes)
            position = self.fp.tell()  # Preserve current position in file
            self.fp.seek(zinfo.header_offset, 0)
            self.fp.write(zinfo.FileHeader(zip64))
            self.fp.seek(position, 0)
        self.filelist.append(zinfo)
        self.NameToInfo[zinfo.filename] = zinfo

    def writestr(self, zinfo_or_arcname, bytes, compress_type=None, pwd=None):
        """Write a file into the archive.  The contents is the string
        'bytes'.  'zinfo_or_arcname' is either a ZipInfo instance or
        the name of the file in the archive."""
        if not isinstance(zinfo_or_arcname, ZipInfo):
            zinfo = ZipInfo(filename=zinfo_or_arcname,
                            date_time=time.localtime(time.time())[:6])

            zinfo.compress_type = self.compression
            if zinfo.filename[-1] == '/':
                zinfo.external_attr = 0o40775 << 16  # drwxrwxr-x
                zinfo.external_attr |= 0x10  # MS-DOS directory flag
            else:
                zinfo.external_attr = 0o600 << 16  # ?rw-------
        else:
            zinfo = zinfo_or_arcname

        if not self.fp:
            raise RuntimeError(
                "Attempt to write to ZIP archive that was already closed")

        if compress_type is not None:
            zinfo.compress_type = compress_type

        zinfo.file_size = len(bytes)  # Uncompressed size
        zinfo.header_offset = self.fp.tell()  # Start of header bytes
        self._writecheck(zinfo)
        self._didModify = True
        zinfo.CRC = crc32(bytes) & 0xffffffff  # CRC-32 checksum
        if zinfo.compress_type == ZIP_DEFLATED:
            co = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION,
                                  zlib.DEFLATED, -15)
            bytes = co.compress(bytes) + co.flush()
            zinfo.compress_size = len(bytes)  # Compressed size
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
            enryption_header = randomFunc(11) + chr(check_byte)
            ze = _ZipEncrypter(pwd)
            bytes = "".join(map(ze, enryption_header + bytes))

        self.fp.write(zinfo.FileHeader(zip64))
        self.fp.write(bytes)
        if zinfo.flag_bits & 0x08:
            # Write CRC and file sizes after the file data
            fmt = '<LQQ' if zip64 else '<LLL'
            self.fp.write(struct.pack(fmt, zinfo.CRC, zinfo.compress_size,
                                      zinfo.file_size))
        self.fp.flush()
        self.filelist.append(zinfo)
        self.NameToInfo[zinfo.filename] = zinfo
