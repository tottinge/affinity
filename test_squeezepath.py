import os
import unittest
from squeezepath import *

class test_squeeze(unittest.TestCase):
    def test_roundtrip(self):
        original =  "a/very/long/file/path/to/squish.down"
        sut = SqueezePath()
        token = sut.encode(original)
        self.failUnless(len(token) < len(original))
        result = sut.decode(token)
        self.assertEqual(original, result)

    def test_paths_compress(self):
        path = "a/very/long/filepath/indeed/jackson/so/deal/with/it"
        sut = SqueezePath()
        for filename in "abcde":
            sut.encode(os.path.join(path,filename))
        self.assertEqual(len("abcde") + 1, len(sut.uniques))

    def test_repeats(self):
        path = "GSX/Gsix/_Tools/magic/fun/stuff/in/python/eat.py"
        sut = SqueezePath()
        first = sut.encode(path)
        second = sut.encode(path)
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
