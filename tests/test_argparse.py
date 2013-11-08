import os
import sys
import unittest
import mimetypes
from analysis.analyze_graph import parse_command_line as parse


class ArgumentsForAnalysis(unittest.TestCase):

    def known_text_file(self):
        filenames = [
            x for x in os.listdir('.')
            if 'text' in str(mimetypes.guess_type(x))
        ]
        return filenames[0]

    def test_with_valid_parameters(self):
        filename = self.known_text_file()
        result = parse("1", "2", filename)
        self.assertEqual(1, result.squelch)
        self.assertEqual(2, result.minsize)
        self.assertEqual(filename, result.inputfile.name)

    def test_verbose_defaults_false(self):
        result = parse("1", "2", self.known_text_file())
        self.assertEquals(False, result.verbose)

    def test_with_long_verbose_parameter(self):
        result = parse('--verbose', "1", "2", self.known_text_file())
        self.assertEquals(True, result.verbose)

    def test_with_short_verbose_parameter(self):
        result = parse('-v', "1", "2", self.known_text_file())
        self.assertEquals(True, result.verbose)

if __name__ == "__main__":
    unittest.main()
