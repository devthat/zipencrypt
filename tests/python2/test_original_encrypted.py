import unittest

from mock import patch

import test_original
from zipencrypt import ZipFile, ZIP_STORED


class AlwaysEncryptZipFile(ZipFile):
    def __init__(self, filename, mode="r", compression=ZIP_STORED, allowZip64=False):
        super(AlwaysEncryptZipFile, self).__init__(filename, mode, compression, allowZip64)
        self.setpassword("password")


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestsWithMultipleOpensEncrypted(test_original.TestsWithMultipleOpens):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestsWithRandomBinaryFilesEncrypted(test_original.TestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestsWithSourceFileEncrypted(test_original.TestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestZip64InSmallFilesEncrypted(test_original.TestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DecryptionTestsEncrypted(test_original.DecryptionTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class OtherTestsEncrypted(test_original.OtherTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class UniversalNewlineTestsEncrypted(test_original.UniversalNewlineTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestWithDirectoryEncrypted(test_original.TestWithDirectory):
    pass


if __name__ == '__main__':
    unittest.main()
