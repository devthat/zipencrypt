import io
import tempfile
import unittest

from zipencrypt import ZipFile, ZipInfo
from zipencrypt.zipencrypt2 import _ZipEncrypter, _ZipDecrypter


class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.plain = "plaintext" * 3
        self.pwd = b"password"

    def test_roundtrip(self):
        encrypt = _ZipEncrypter(self.pwd)
        encrypted = map(encrypt, self.plain)

        decrypt = _ZipDecrypter(self.pwd)
        decrypted = "".join(map(decrypt, encrypted))

        self.assertEqual(self.plain, decrypted)


class TestZipfile(unittest.TestCase):
    def setUp(self):
        self.zipfile = io.BytesIO()
        self.plain = "plaintext" * 3
        self.pwd = "password"

    def test_writestr(self):
        with ZipFile(self.zipfile, mode="w") as zipfd:
            zipfd.writestr("file1.txt", self.plain, pwd=self.pwd)
        with ZipFile(self.zipfile) as zipfd:
            content = zipfd.read("file1.txt", pwd=self.pwd)

        self.assertEqual(self.plain, content)

    def test_writestr_keep_file_open(self):
        with ZipFile(self.zipfile, mode="w") as zipfd:
            zipfd.writestr("file1.txt", self.plain, pwd=self.pwd)
            content = zipfd.read("file1.txt", pwd=self.pwd)

        self.assertEqual(self.plain, content)

    def test_writestr_with_zipinfo(self):
        zinfo = ZipInfo(filename="file1.txt")
        zinfo.flag_bits |= 0x8

        with ZipFile(self.zipfile, mode="w") as zipfd:
            zipfd.writestr(zinfo, self.plain, pwd=self.pwd)
        with ZipFile(self.zipfile) as zipfd:
            content = zipfd.read("file1.txt", pwd=self.pwd)

        self.assertEqual(self.plain, content)

    def test_writestr_with_zipinfo_keep_file_open(self):
        zinfo = ZipInfo(filename="file1.txt")
        zinfo.flag_bits |= 0x8

        with ZipFile(self.zipfile, mode="w") as zipfd:
            zipfd.writestr(zinfo, self.plain, pwd=self.pwd)
            content = zipfd.read("file1.txt", pwd=self.pwd)

        self.assertEqual(self.plain, content)

    def test_write_with_password(self):
        with tempfile.NamedTemporaryFile(bufsize=0) as fd:
            fd.write(self.plain)

            with ZipFile(self.zipfile, mode="w") as zipfd:
                zipfd.write(fd.name, arcname="file1.txt", pwd=self.pwd)
            with ZipFile(self.zipfile) as zipfd:
                content = zipfd.read("file1.txt", pwd=self.pwd)

        self.assertEqual(self.plain, content)

    def test_write_with_password_keep_file_open(self):
        with tempfile.NamedTemporaryFile(bufsize=0) as fd:
            fd.write(self.plain)

            with ZipFile(self.zipfile, mode="w") as zipfd:
                zipfd.write(fd.name, arcname="file1.txt", pwd=self.pwd)
                content = zipfd.read("file1.txt", pwd=self.pwd)

        self.assertEqual(self.plain, content)


if __name__ == '__main__':
    unittest.main()
