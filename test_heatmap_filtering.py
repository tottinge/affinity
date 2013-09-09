import unittest
from collections import defaultdict
import heatmap

class testFiltering(unittest.TestCase):
    unfiltered = {
        "":[],
        "a.cpp":["DE123","US123","DE000","US999"],
        "b.cpp":[],
        "c.cpp":["DE123","DE000","US999"],
        "d.cpp":["DE123","DE000","US999"],
        "e.cpp":["DE123","US123"],
        "x.py":["DE1","DE2","DE3"],

    }
    unfiltered_keys = set(unfiltered.keys())

    def test_singleFilter(self):
        filtered = heatmap.filter_by_keyword(self.unfiltered, ["cpp"])
        result = dict(filtered)
        self.assertEqual(set(result.keys()), set(["a.cpp","b.cpp","c.cpp","d.cpp","e.cpp"]))

    def test_doubleFilter(self):
        filtered = dict(
            heatmap.filter_by_keyword(self.unfiltered, ["cpp","py"])
        )
        dropped = self.unfiltered_keys.difference(filtered.keys())
        self.assertEqual(set(['']), dropped)

if __name__ == "__main__":
    unittest.main()
