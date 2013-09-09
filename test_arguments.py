import sys
import unittest
import heatmap

class ArgumentParser(unittest.TestCase):
    """Test handling of command line arguments by heatmap.py"""

    def test_worksWithNoArguments(self):
        parse = heatmap.handle_arguments([])
        self.assertTrue(parse.filters is None)
        self.assertEqual(parse.files, [])

    def test_CanDetectFilterFile(self):
        try:
            parse = heatmap.handle_arguments(["-f","names"])
        except Exception as e:
            self.fail(str(e))
        self.assertEqual(parse.filters, "names")

    def test_defaultsToNoFilter(self):
        parse = heatmap.handle_arguments([])
        self.assertTrue(parse.filters is None)

    def test_undecoratedArgumentsBecomeFileList(self):
        commandLine = ["first","second","third"]
        parse = heatmap.handle_arguments(commandLine)
        self.assertEqual(parse.files, commandLine)

if __name__ == '__main__':
    unittest.main()

