import unittest
import heatmap

divider=heatmap.divider

class test_with_listcheck(unittest.TestCase):
    def assertIn(self, element, container):
        self.failUnless(element in container, "Expected %s in [%s]" % (element, container))
    def assertItemsEqual(self, left, right):
        self.assertEqual(sorted(left), sorted(right))

class TestPattern(test_with_listcheck):
    def test_finds_ticket(self):
        actual = heatmap.ticketsFromDescription(' ticket US1111 nonsense')
        self.assertEqual(actual, set(['US1111']) )

    def test_case_insensitive(self):
        actual = heatmap.ticketsFromDescription('de11 us22')
        self.assertEqual(actual, set(['de11','us22']))

    def test_finds_no_ticket(self):
        actual = heatmap.ticketsFromDescription('tickets to us 111 times 232 bus45 tirade 3043')
        self.assertEqual(actual, set())

    def test_finds_multiple_tickets_in_record(self):
        actual = heatmap.ticketsFromDescription("us34322:de2322 = us 102")
        self.assertEqual(actual, set(["us34322","de2322"]))

class TestStreamReader(test_with_listcheck):
    def test_emptyStreamIsOkay(self):
        self.assertRaises(StopIteration, lambda:heatmap.next_changeset(iter([])) )

    def test_ticket_with_one_file(self):
        x = heatmap.next_changeset(iter([
            "de7877\n",
            divider,
            "file1\n",
            "\n"
            ]))
        self.assertEquals(x.tickets, ['DE7877'])
        self.assertEquals(x.files, ['file1'])

    def test_three_tickets_and_one_file(self):
        x = heatmap.next_changeset(iter([
            "this is my ticket DE8909 and yours is US4333\n",
            divider,
            "file2.py\n",
            "file1.cpp\n",
            ""
            ]))
        self.assertEquals(sorted(x.tickets), ['DE8909','US4333'])
        self.assertEquals(sorted(x.files), ['file1.cpp','file2.py'])

    def test_sequential_record_parse(self):
        data = iter([
            "DE1222: Fix use of parenthesis",
            divider,
            "parrot.py",
            "scurvy.py",
            "booty.cpp",
            "",
            "US32 - allow users to enter a birthdate",
            divider,
            "parrot.py",
            "screen.ui",
            "dateUtil.py",
            "ageapi.h",
            "ageapi.cpp",
            ""
        ])
        r1 = heatmap.next_changeset(data)
        r2 = heatmap.next_changeset(data)
        self.assertEqual(r2.tickets, ["US32"])
        self.assertIn("parrot.py", r2.files)
        self.assertIn("screen.ui", r2.files)

    def test_emits_records(self):
        data = iter([
            "US12 - do something",
            divider,
            "us12_file1.py",
            "us12_file2.py",
            "",
            "DE11 - fix me",
            divider,
            "de1_file1.cpp",
            "de1_file2.h",
            ""
        ])
        actual = [ result for result in heatmap.gather_changesets(data) ]

        expected_first = heatmap.RecordResult(
            ['US12'],
            ['us12_file1.py','us12_file2.py']
        )
        self.assertEqual(actual[0], expected_first)
        
        expected_second = heatmap.RecordResult(['DE11'],['de1_file1.cpp','de1_file2.h'])
        self.assertEqual(actual[1], expected_second)

class heatCalculation(test_with_listcheck):

    def test_nothingToTalkAbout(self):
        self.assertEquals((0,0), heatmap.calculate_heat("me", []))

    def test_allDefects(self):
        self.assertEquals((1,1), heatmap.calculate_heat("me", ["DE100"]))

    def test_noDefects(self):
        self.assertEquals((1,0), heatmap.calculate_heat("me", ["US1232"]))

    def test_prepareForDisplay_ignoresUnticketedChangesets(self):
        input = { 
            "/Heat4:3/":["DE3","US1","DE1","DE2"],
            "/Heat4:0/":["US1","US1","US2","US3"],
            "/Heat3:3/":["DE2","DE1","DE3"],
            "/ignored/":[],
        }
        values = [x for x in heatmap.prepareForDisplay(input.iteritems())]
        expected = [
            (4,3,"/Heat4:3/",["DE1","DE2","DE3","US1"]),
            (4,0,"/Heat4:0/",["US1","US1","US2","US3"]),
            (3,3,"/Heat3:3/",["DE1","DE2","DE3"]),
        ]
        self.assertItemsEqual(values,expected)

    def test_sequential_record_parse(self):
        data = iter([
            "DE1222: Fix use of parenthesis",
            divider,
            "parrot.py",
            "scurvy.py",
            "booty.cpp",
            "",
            "US32 - allow users to enter a birthdate",
            divider,
            "parrot.py",
            "screen.ui",
            "dateUtil.py",
            "ageapi.h",
            "ageapi.cpp",
            "\n"
        ])
        r1 = heatmap.next_changeset(data)
        r2 = heatmap.next_changeset(data)
        self.assertEqual(r2.tickets, ["US32"])
        self.assertIn("parrot.py", r2.files)
        self.assertIn("screen.ui", r2.files)

        

if __name__ == '__main__':
    unittest.main()

