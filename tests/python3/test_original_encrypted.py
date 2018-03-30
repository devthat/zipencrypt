import unittest
from unittest.mock import patch

import test_original
from zipencrypt import ZipFile, ZIP_STORED


class AlwaysEncryptZipFile(ZipFile):
    def __init__(self, filename, mode="r", compression=ZIP_STORED, allowZip64=False):
        super(AlwaysEncryptZipFile, self).__init__(filename, mode, compression, allowZip64)
        self.setpassword(b"password")


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredTestsWithSourceFileEncrypted(test_original.StoredTestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateTestsWithSourceFileEncrypted(test_original.DeflateTestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2TestsWithSourceFileEncrypted(test_original.Bzip2TestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaTestsWithSourceFileEncrypted(test_original.LzmaTestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredTestZip64InSmallFilesEncrypted(
    test_original.StoredTestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateTestZip64InSmallFilesEncrypted(test_original.DeflateTestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2TestZip64InSmallFilesEncrypted(test_original.Bzip2TestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaTestZip64InSmallFilesEncrypted(test_original.LzmaTestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class ExtractTestsEncrypted(test_original.ExtractTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class OtherTestsEncrypted(test_original.OtherTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredBadCrcTestsEncrypted(test_original.StoredBadCrcTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateBadCrcTestsEncrypted(test_original.DeflateBadCrcTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2BadCrcTestsEncrypted(test_original.Bzip2BadCrcTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaBadCrcTestsEncrypted(test_original.LzmaBadCrcTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DecryptionTestsEncrypted(test_original.DecryptionTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredTestsWithRandomBinaryFilesEncrypted(test_original.StoredTestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateTestsWithRandomBinaryFilesEncrypted(test_original.DeflateTestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2TestsWithRandomBinaryFilesEncrypted(test_original.Bzip2TestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaTestsWithRandomBinaryFilesEncrypted(
    test_original.LzmaTestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class UnseekableTestsEncrypted(test_original.UnseekableTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestsWithMultipleOpensEncrypted(test_original.TestsWithMultipleOpens):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestWithDirectoryEncrypted(test_original.TestWithDirectory):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class StoredUniversalNewlineTestsEncrypted(test_original.StoredUniversalNewlineTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DeflateUniversalNewlineTestsEncrypted(test_original.DeflateUniversalNewlineTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class Bzip2UniversalNewlineTestsEncrypted(test_original.Bzip2UniversalNewlineTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class LzmaUniversalNewlineTestsEncrypted(test_original.LzmaUniversalNewlineTests):
    pass


if __name__ == '__main__':
    unittest.main()
