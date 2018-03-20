import unittest

from mock import patch

import test_original
from zipencrypt import ZipFile, ZIP_STORED


class AlwaysEncryptZipFile(ZipFile):
    def __init__(self, filename, mode="r", compression=ZIP_STORED,
                 allowZip64=False):
        super(AlwaysEncryptZipFile, self).__init__(
            filename, mode, compression, allowZip64)
        self.setpassword("password")


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestsWithMultipleOpens2(test_original.TestsWithMultipleOpens):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestsWithRandomBinaryFiles2(test_original.TestsWithRandomBinaryFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestsWithSourceFile2(test_original.TestsWithSourceFile):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestZip64InSmallFiles2(test_original.TestZip64InSmallFiles):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class DecryptionTests2(test_original.DecryptionTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class OtherTests2(test_original.OtherTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class UniversalNewlineTests2(test_original.UniversalNewlineTests):
    pass


@patch("zipencrypt.ZipFile", AlwaysEncryptZipFile)
class TestWithDirectory2(test_original.TestWithDirectory):
    pass


if __name__ == '__main__':
    unittest.main()
