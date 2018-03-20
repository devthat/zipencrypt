import unittest

from mock import patch

import test_zipfile
from zipfile2 import ZipFile, ZIP_STORED


class AlwaysEncryptZipFile(ZipFile):
    def __init__(self, filename, mode="r", compression=ZIP_STORED,
                 allowZip64=False):
        super(AlwaysEncryptZipFile, self).__init__(
            filename, mode, compression, allowZip64)
        self.setpassword("password")


@patch("zipfile2.ZipFile", AlwaysEncryptZipFile)
class TestsWithMultipleOpens2(test_zipfile.TestsWithMultipleOpens):
    pass


@patch("zipfile2.ZipFile", AlwaysEncryptZipFile)
class TestsWithRandomBinaryFiles2(test_zipfile.TestsWithRandomBinaryFiles):
    pass


@patch("zipfile2.ZipFile", AlwaysEncryptZipFile)
class TestsWithSourceFile2(test_zipfile.TestsWithSourceFile):
    pass


@patch("zipfile2.ZipFile", AlwaysEncryptZipFile)
class TestZip64InSmallFiles2(test_zipfile.TestZip64InSmallFiles):
    pass


@patch("zipfile2.ZipFile", AlwaysEncryptZipFile)
class DecryptionTests2(test_zipfile.DecryptionTests):
    pass


@patch("zipfile2.ZipFile", AlwaysEncryptZipFile)
class OtherTests2(test_zipfile.OtherTests):
    pass


@patch("zipfile2.ZipFile", AlwaysEncryptZipFile)
class UniversalNewlineTests2(test_zipfile.UniversalNewlineTests):
    pass


@patch("zipfile2.ZipFile", AlwaysEncryptZipFile)
class TestWithDirectory2(test_zipfile.TestWithDirectory):
    pass


if __name__ == '__main__':
    unittest.main()
