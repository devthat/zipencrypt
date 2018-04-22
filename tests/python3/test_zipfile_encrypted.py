import unittest
from unittest.mock import patch

import test_zipfile

from zipencrypt import ZipFile, ZIP_STORED


class AlwaysEncryptZipFile(ZipFile):
    def __init__(self, filename, mode="r", compression=ZIP_STORED, allowZip64=False):
        super(AlwaysEncryptZipFile, self).__init__(filename, mode, compression, allowZip64)
        self.setpassword(b"password")


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredTestsWithSourceFileEncrypted(test_zipfile.StoredTestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateTestsWithSourceFileEncrypted(test_zipfile.DeflateTestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2TestsWithSourceFileEncrypted(test_zipfile.Bzip2TestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaTestsWithSourceFileEncrypted(test_zipfile.LzmaTestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredTestZip64InSmallFilesEncrypted(test_zipfile.StoredTestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateTestZip64InSmallFilesEncrypted(test_zipfile.DeflateTestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2TestZip64InSmallFilesEncrypted(test_zipfile.Bzip2TestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaTestZip64InSmallFilesEncrypted(test_zipfile.LzmaTestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredWriterTestsEncrypted(test_zipfile.StoredWriterTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateWriterTestsEncrypted(test_zipfile.DeflateWriterTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2WriterTestsEncrypted(test_zipfile.Bzip2WriterTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaWriterTestsEncrypted(test_zipfile.LzmaWriterTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class ExtractTestsEncrypted(test_zipfile.ExtractTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class OtherTestsEncrypted(test_zipfile.OtherTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredBadCrcTestsEncrypted(test_zipfile.StoredBadCrcTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateBadCrcTestsEncrypted(test_zipfile.DeflateBadCrcTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2BadCrcTestsEncrypted(test_zipfile.Bzip2BadCrcTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaBadCrcTestsEncrypted(test_zipfile.LzmaBadCrcTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DecryptionTestsEncrypted(test_zipfile.DecryptionTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredTestsWithRandomBinaryFilesEncrypted(test_zipfile.StoredTestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateTestsWithRandomBinaryFilesEncrypted(test_zipfile.DeflateTestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2TestsWithRandomBinaryFilesEncrypted(test_zipfile.Bzip2TestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaTestsWithRandomBinaryFilesEncrypted(test_zipfile.LzmaTestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class UnseekableTestsEncrypted(test_zipfile.UnseekableTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestsWithMultipleOpensEncrypted(test_zipfile.TestsWithMultipleOpens):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestWithDirectoryEncrypted(test_zipfile.TestWithDirectory):
    pass


if __name__ == '__main__':
    unittest.main()
