""" Some code to handle 2.6+ and 3.* compatibility. """
from __future__ import print_function, unicode_literals
import sys

if sys.version_info > (3,):
    long = int

if sys.version_info < (3,):
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes
