zipencrypt
==========

zipencrypt is a Python module to provide *weak* password-based
encryption for zipfiles. It is meant as a drop-in replacement for
zipfile from the standard lib and provides the counterpart to the
decryption implemented there.

It is implemented in pure python and does not rely on any 3rd party libraries.

Compatible to python 2.7 and 3.4+

Installation
------------

::

    pip install zipencrypt

The code
--------

.. code:: python

    from zipencrypt import ZipFile

    with ZipFile("file.zip", mode="w") as f:
        f.writestr("file1.txt", "plaintext", pwd=b"password")

Do not use this!
----------------

The standard encryption of ZIP is known to be seriously flawed (see
`here <https://en.wikipedia.org/wiki/Zip_(file_format)#Encryption>`_).
That is probably the reason why it is not implemented in zipfile in the
standard lib. There are however legitimate use cases.
