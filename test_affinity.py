import unittest
from affinities import *
from hg_log_parser import divider as SEPARATOR
#SEPARATOR = "-^-^*"

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
        edge,weight = edges.popitem()
        self.assertEquals('file1.cpp', edge.left)
        self.assertEquals('file2.cpp', edge.right)
        self.assertEqual(weight,1)

    def test_ignoring_noise_from_merge_records(self):
        records = [
            "Merge should be discarded",
            SEPARATOR,
            "file1.cpp",
            "file2.cpp",
            ""
        ]
        edges = get_weighted_edges(iter(records))
        self.assertEqual(0, len(edges))

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

    def test_weight_counter_with_reverse_node(self):
        records = [
            "US00001: Two files makes one edge",
            SEPARATOR,
            "file1.cpp",
            "file2.cpp",
            "",
            "US00002: Two files in reverse still makes same edge",
            SEPARATOR,
            "file2.cpp",
            "file1.cpp",
            ""
        ] 
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


class EdgeClassTests(unittest.TestCase):
    def test_creation(self):
        e = Edge( "a","b")
        self.assertEquals('a', e.left)
        self.assertEquals('b', e.right)
    def test_compression(self):
        x = "a/very/long/file/directory/path/thatExtends/into/the/file/system/for/miles"
        left = os.path.join(x, "left.cpp")
        right = os.path.join(x, "right.cpp")
        e = Edge(left,right)
        len(e.short) < (len(left)+len(right))
    def test_identity(self):
        x = Edge("a/path/to/x", "a/path/to/y")
        y = Edge("a/path/to/x", "a/path/to/y")
        self.assertEquals(x,y)
    def test_usable_as_dict_key(self):
        x = Edge("a/path/to/x", "a/path/to/y")
        y = Edge("a/path/to/x", "a/path/to/y")
        result = {x:1}
        result[y] = 2
        self.assertEquals(1, len(result))

class DropUninterestingFiles(unittest.TestCase):
    def test_source_files_pass_through(self):
        safe_ext =  [
            'cpp'
            , 'h'
            , 'ui'
            , 'xml'
            , 'txt'
            , 'feature'
            , 'py'
            , 'sh'
            , 'sql'
        ]
        file_list = [ "this." + ext for ext in safe_ext]
        self.assertEquals(file_list, list(interesting_files(file_list)))
    def ignore_test_unwanted_files_are_stripped(self):
        dull_ext =  [
            'png'
            , 'pyc'
            , 'ts'
            , 'htm'
            , 'hhc'
            , 'ini'
        ]
        file_list = [ 'bad.' + ext for ext in dull_ext ]
        self.assertEquals([], list(interesting_files(file_list)))


if __name__ == "__main__":
    unittest.main()
