import unittest
from Generate import *
dummyReportData = [(0,0,'zero')]
class test_with_listcheck(unittest.TestCase):
    def assertIn(self, element, container):
        self.failUnless(element in container, "Expected %s in [%s]" % (element, container))
    def assertItemsEqual(self, left, right):
        self.assertEqual(sorted(left), sorted(right))

class test_color_selection(test_with_listcheck):
    def setUp(self):
        self.report = Report(dummyReportData)
    def test_gets_maximum_red_for_max(self):
        report = self.report
        self.assertEqual(report._get_color(100,100), acceptable_reds[-1])
    def test_lowest_red_for_zero(self):
        report = self.report
        self.assertEqual(report._get_color(0,100), acceptable_reds[0])
    def test_half_red_for_half_value(self):
        report = self.report
        middle = int((len(acceptable_reds)-1)/2.0)
        item = acceptable_reds[middle]
        actual = report._get_color(50,100)
        self.assertEqual(actual, item, "Expected %d got %d" % (middle,acceptable_reds.index(actual)))

class test_size_selection(test_with_listcheck):
    def test_maximum_size_for_max(self):
        report = Report(dummyReportData)
        self.assertEqual(report._get_size(100,100), text_sizes[-1])
    def test_minimum_size(self):
        report = Report(dummyReportData)
        self.assertEqual(report._get_size(0,100), text_sizes[0])
    def test_half_red_for_half_value(self):
        report = Report(dummyReportData)
        middle = len(text_sizes)/2
        self.assertEqual(report._get_size(51,100), text_sizes[middle])

class test_style(test_with_listcheck):
    def test_basic_formatting(self):
        report = Report(dummyReportData)
        result = report._link_styling("/x/y/z", 1, 5, 'green', 'huge')
        self.assertIn('green', result)
        self.assertIn('huge', result)
        self.assertIn('x/y/z', result)
        self.assertIn('href', result)
        self.assertIn('>z</a></li>', result)

class test_analysis(test_with_listcheck):
    data = [
       ( 2, 1, "/x/y/nice.py"),
       (22,20, "/x/y/horrible.cs"),
       (30,15, "/x/y/somewhat_ugly.cpp"),
       (12,12, "/x/y/awful.cpp"),
       (15, 5, "/x/y/comma,check.cpp"),
    ]
    def test_collection(self):
        report = Report(self.data)
        self.assertEqual(report.most_changed, 30)

class test_datadisplay(test_with_listcheck):
    def test_create_report(self):
        data = [
            ( 2, 1, "/x/y/nice.py"),
            (22,20, "/x/y/horrible.cs"),
            (30,15, "/x/y/somewhat_ugly.cpp"),
            (12,12, "/x/y/awful.cpp"),
            (15, 5, "/x/y/comma,check.cpp"),
        ]
        report = Report(data)
        xml = report.generate_html()
        

if __name__ == "__main__":
    unittest.main()
