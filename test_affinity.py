import unittest
from affinities import *
SEPARATOR = "-^-^*"

class TestCounter(unittest.TestCase):
    def test_null_input(self):
        edges = get_weighted_edges(iter([]))
        self.failUnless(len(edges)==0)

    def test_one_file(self):
        records = [
            "US00000: One file does not an edge make",
            SEPARATOR,
            "file1.cpp",
            ""
        ]
        edges = get_weighted_edges(iter(records))
        self.assertEqual(len(edges), 0) 

    def test_one_edge(self):
        records = [
            "US00001: Two files makes one edge",
            SEPARATOR,
            "file1.cpp",
            "file2.cpp",
            ""
        ]
        edges = get_weighted_edges(iter(records))
        self.assertEqual(len(edges), 1) 
        files,weight = edges.popitem()
        self.failUnless('file1.cpp' in files)
        self.failUnless('file2.cpp' in files)
        self.assertEqual(weight,1)

    def test_weight_counter(self):
        records = [
            "US00001: Two files makes one edge",
            SEPARATOR,
            "file1.cpp",
            "file2.cpp",
            ""
        ] * 2
        edges = get_weighted_edges(iter(records))
        self.assertEqual(len(edges), 1) 
        _,weight = edges.popitem()
        self.assertEqual(2, weight)

    def test_combinations(self):
        records = [
            "US3: three records = three combinations",
            SEPARATOR,
            "A.h",
            "B.h",
            "C.h",
            ""
        ]
        # should be: a-b, b-c, a-c order doesn't matter
        edges = get_weighted_edges(iter(records))
        self.assertEqual(3, len(get_weighted_edges(iter(records)))) 

class test_significance(unittest.TestCase):
    def test_null(self):
        result = toss_least_significant({})
        self.assertEqual(result, {})
    def test_one_is_never_significant(self):
        result = toss_least_significant({
            ("a","b"): 1
        })
        self.assertEqual(result, {})
    def test_largest_greater_than_1_is_signifcant(self):
        result = toss_least_significant({
            ("a","b"): 1,
            ("b","c"): 5
        })
        self.assertEqual(result, {("b","c"):5})

    def test_half_of_average_is_insignificant(self):
        weights = [2,3,5,8,13,21]
        half_mean = ( sum(weights)/len(weights)) * .5

        inputs = dict( ((weight,weight), weight) for weight in weights)
        result = toss_least_significant(inputs)

        under_half = [ weight for (_,weight) in result.iteritems()
                       if weight < half_mean ]
        self.assertEqual([], under_half)




if __name__ == "__main__":
    unittest.main()
