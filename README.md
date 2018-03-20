# What is it?
zipencrypt is a Python module to provide *weak* encryption for zipfiles. 
It is meant as a drop-in replacement for zipfile from the standard lib and 
provides the counterpart to the decryption implemented there.

# Do not use this!
The standard encryption of ZIP is known to be seriously flawed (see [here](https://en.wikipedia.org/wiki/Zip_(file_format)#Encryption)).
That is probably the reason why it is not implemented in zipfile in the standard lib.
There are however legitimate use cases.
