import unittest
from matchable import *

class TestParser(unittest.TestCase):
    def test_null_file(self):
        log = iter([])
        result = list(gather_changes(log))
        self.assertEqual(len(result), 0)

    def test_one_record_collected(self):
        log = iter([
            "author",
            "2013-08-10",
            divider,
            ""
        ])
        result = list(gather_changes(log))
        self.assertEqual(1, len(result))

    def test_two_records_collected(self):
        log = iter([
            "author",
            "2013-08-10",
            divider,
            ""
        ] * 2)
        result = list(gather_changes(log))
        self.assertEqual(2, len(result))

    def test_author_collected(self):
        log = iter([
            "Joe@example.com",
            "2013-08-10",
            divider,
            ""
        ])
        result = list(gather_changes(log))
        self.assertEqual("Joe@example.com", result[0].author)

    def test_date_collected(self):
        log = iter([
            "author",
            "2013-08-10",
            divider,
            ""
        ])
        result = list(gather_changes(log))
        self.assertEqual("2013-08-10", result[0].date)

    def test_tickets(self):
        log = iter([
            "author",
            "2013-08-10",
            "Tickets for US80 US74 US65 DE222 satisfied",
            divider,
            ""
        ])
        result = list(gather_changes(log))
        tickets = result[0].tickets
        self.assertTrue('US80' in tickets)
        self.assertTrue('US74' in tickets)
        self.assertTrue('US65' in tickets)
        self.assertTrue('DE222' in tickets)

    def test_tickets_on_multiple_lines(self):
        log = iter([
            "author",
            "2013-08-10",
            "Tickets for US80 ",
            "   US74 ",
            "   US65 DE222 satisfied",
            divider,
            ""
        ])
        result = list(gather_changes(log))
        tickets = result[0].tickets
        self.assertTrue('US80' in tickets)
        self.assertTrue('US74' in tickets)
        self.assertTrue('US65' in tickets)
        self.assertTrue('DE222' in tickets)

    def test_files_collected(self):
        log = iter([
            "author",
            "2013-02-01",
            "desc",
            divider,
            "   file1",
            "   file2",
            ""
        ])
        result = list(gather_changes(log))
        files = result[0].files
        self.assertTrue('file1' in files)
        self.assertTrue('file2' in files)

    

if __name__ == "__main__":
    unittest.main()
