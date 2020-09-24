#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2020-09-24 20:21:23 vk>

# FIXXME: remove unnecessary imports
import unittest
import orgdepend_to_orgedna


class TestMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_trigger_regex_matches(self):

        # FIXXME: do not only check match/non-match but also number of matching elements:

        # normal org-depend lines:
        self.assertEqual(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER:    2016-11-04-some-title(DONE)'),
                        [('2016-11-04-some-title', 'DONE')])
        self.assertEqual(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER: 2016-11-04-some-title(DONE)'),
                        [('2016-11-04-some-title', 'DONE')])
        self.assertEqual(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER: 2016-11-04-some-title(DONE)  2020-09-19-foo(STARTED)'),
                        [('2016-11-04-some-title', 'DONE'), ('2020-09-19-foo', 'STARTED')])

        # yasnippet version of a trigger line:
        self.assertEqual(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER: prefix-`(my-capture-insert \'my-1)`-notes(STARTED)'),
                         [('prefix-`(my-capture-insert \'my-1)`-notes', 'STARTED')])
        self.assertEqual(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER: prefix-`(my-capture-insert \'my-1)`-notes(STARTED)    prefix2-`(my-capture-insert \'my-foo)`-bar(NEXT)'),
                         [('prefix-`(my-capture-insert \'my-1)`-notes', 'STARTED'), ('prefix2-`(my-capture-insert \'my-foo)`-bar', 'NEXT')])

        # chain-siblings
        self.assertEqual(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER: chain-siblings(NEXT)'),
                        [('chain-siblings', 'NEXT')])

        # org-depend lines that are not "active":
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches(': :TRIGGER:    2016-11-04-some-title(DONE)'))
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches('.:TRIGGER: 2016-11-04-some-title(DONE)'))
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches(':noTRIGGER: 2016-11-04-some-title(DONE)  2020-09-19-foo(STARTED)'))

        # org-edna lines
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER: ids("id:2020-07-09-new-heading-5") todo!(NEXT) scheduled!(".") ids("id:2020-07-09-new-heading-6") todo!(NEXT) scheduled!("++2d")'))
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER:  ids("id:GProj-Celebrate-and-close-project") todo!(NEXT) scheduled!(".")'))
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER: ids("id:taskD") scheduled!(".") todo!(WAITING)'))
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches(':TRIGGER: ids("id:2020-07-11-org-super-links") scheduled!(".")'))

        # org-edna lines that are not "active":
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches(': :TRIGGER: ids("id:2020-09-19-foo-bar") todo!(NEXT)'))
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches(':noTRIGGER: ids("id:2020-09-19-foo-bar") todo!(NEXT)'))
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches('#:TRIGGER: ids("id:2020-09-19-foo-bar") todo!(NEXT)'))
        self.assertFalse(orgdepend_to_orgedna.get_trigger_matches('.:TRIGGER: ids("id:2020-09-19-foo-bar") todo!(NEXT)'))

    def test_blocker_regex_matches(self):

        # normal org-depend lines:
        self.assertEqual(['2016-11-04-some-title'], orgdepend_to_orgedna.get_blocker_matches(':BLOCKER:    2016-11-04-some-title'))
        self.assertEqual(['2016-11-04-some-title'], orgdepend_to_orgedna.get_blocker_matches('   :BLOCKER:    2016-11-04-some-title'))
        self.assertEqual(['2016-11-04-some-title'], orgdepend_to_orgedna.get_blocker_matches(':BLOCKER: 2016-11-04-some-title  '))
        self.assertEqual(['2016-11-04-some-title', '2020-09-19-foo'], orgdepend_to_orgedna.get_blocker_matches(' :BLOCKER: 2016-11-04-some-title  2020-09-19-foo'))
        self.assertEqual(['2016-11-04-some-title', '2020-09-19-foo'], orgdepend_to_orgedna.get_blocker_matches(':BLOCKER: 2016-11-04-some-title, 2020-09-19-foo'))
        self.assertEqual(['2016-11-04-some-title', '2020-09-19-foo'], orgdepend_to_orgedna.get_blocker_matches(':BLOCKER: 2016-11-04-some-title,  2020-09-19-foo'))

        # with yasnippet code in it:
        self.assertEqual(['`(my-capture-insert \'my-event-date)`-k-email1'], orgdepend_to_orgedna.get_blocker_matches(':BLOCKER: `(my-capture-insert \'my-event-date)`-k-email1'))
        self.assertEqual(['prefix-`(my-capture-insert \'my-1)`-notes', 'prefix2-`(my-capture-insert \'my-foo)`-bar'],
                         orgdepend_to_orgedna.get_blocker_matches(':BLOCKER: prefix-`(my-capture-insert \'my-1)`-notes prefix2-`(my-capture-insert \'my-foo)`-bar'))
        self.assertEqual(['prefix-`(my-capture-insert \'my-1)`-notes', 'prefix2-`(my-capture-insert \'my-foo)`-bar'],
                         orgdepend_to_orgedna.get_blocker_matches(':BLOCKER: prefix-`(my-capture-insert \'my-1)`-notes  prefix2-`(my-capture-insert \'my-foo)`-bar'))

        # org-depend lines that are not "active":
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(': :BLOCKER: 2016-11-04-some-title'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches('#+:BLOCKER: 2016-11-04-some-title'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(':noBLOCKER: 2016-11-04-some-title'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches('#COMMENT# :BLOCKER: 2016-11-04-some-title'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches('. :BLOCKER: 2016-11-04-some-title'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches('- :BLOCKER: 2016-11-04-some-title'))

        # org-edna lines
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(':BLOCKER: ids("id:2020-09-19-foo-bar")'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(':BLOCKER:     ids("id:2020-09-19-foo-bar")'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(' :BLOCKER: ids("id:2020-09-19-foo-bar")'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches('   :BLOCKER:     ids("id:2020-09-19-foo-bar")'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(':BLOCKER:  ids("id:2020-09-19-foo-bar" "id:2020-09-19-baz")'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(':BLOCKER:  ids("id:2020-09-19-foo-bar"  "id:2020-09-19-baz")'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(':BLOCKER:  ids(2020-09-19-foo-bar 2020-09-19-baz)'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(':BLOCKER:  ids("id:2020-09-19-foo-bar" 2020-09-19-baz)'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(':BLOCKER:  ids(2020-09-19-foo-bar  2020-09-19-baz)'))

        # org-edna lines that are not "active":
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(': :BLOCKER: ids("id:2020-09-19-foo-bar")'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches(':noBLOCKER: ids("id:2020-09-19-foo-bar")'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches('#:BLOCKER: ids("id:2020-09-19-foo-bar")'))
        self.assertEqual(None, orgdepend_to_orgedna.get_blocker_matches('.:BLOCKER: ids("id:2020-09-19-foo-bar")'))

    def test_simple_trigger_line(self):

        self.assertEqual(orgdepend_to_orgedna.convert_trigger_line([('2016-11-04-some-title', 'DONE')]),
                         ':TRIGGER: ids("id:2016-11-04-some-title") todo!(DONE)')

    def test_trigger_with_chain_siblings(self):

        self.assertEqual(orgdepend_to_orgedna.convert_trigger_line([('chain-siblings', 'NEXT')]),
                         ':TRIGGER: next-sibling todo!(NEXT)')

    def test_trigger_line_with_two_ids(self):

        self.assertEqual(orgdepend_to_orgedna.convert_trigger_line([('2016-11-04-some-title', 'DONE'), ('2020-09-19-foo', 'STARTED')]),
                         ':TRIGGER: ids("id:2016-11-04-some-title") todo!(DONE) ids("id:2020-09-19-foo") todo!(STARTED)')

    def test_trigger_line_with_elisp_snippet(self):

        self.assertEqual(orgdepend_to_orgedna.convert_trigger_line([('prefix-`(my-capture-insert \'my-1)`-notes', 'STARTED'), ('prefix2-`(my-capture-insert \'my-foo)`-bar', 'NEXT')]),
                         ':TRIGGER: ids("id:prefix-`(my-capture-insert \'my-1)`-notes") todo!(STARTED) ids("id:prefix2-`(my-capture-insert \'my-foo)`-bar") todo!(NEXT)'
                         )

    def test_convert_simple_blocker_line(self):

        self.assertEqual(orgdepend_to_orgedna.generate_blocker_line_from_ids(['2015-07-19-an-id']),
                         ':BLOCKER: ids("id:2015-07-19-an-id")'
                         )

    def test_convert_blocker_2_ids(self):

        self.assertEqual(orgdepend_to_orgedna.generate_blocker_line_from_ids(['2015-07-19-an-id', '2020-09-19-another']),
                         ':BLOCKER: ids("id:2015-07-19-an-id" "id:2020-09-19-another")'
                         )

    def test_yasnippet_blocker(self):

        self.assertEqual(orgdepend_to_orgedna.generate_blocker_line_from_ids(['`(my-capture-insert \'my-event-date)`-k-email1']),
                                                                             ':BLOCKER: ids("id:`(my-capture-insert \'my-event-date)`-k-email1")')

if __name__ == '__main__':
    unittest.main()
