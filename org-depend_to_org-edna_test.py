#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2020-09-19 12:03:15 vk>

## FIXXME: remove unnecessary imports
import unittest
#import os
import org-depend_to_org-edna
#import tempfile
#import os.path
import logging
#import platform
#import time  # for sleep()
#from shutil import rmtree

# TEMPLATE for debugging:
#        try:
#        except AssertionError:
#            import pdb; pdb.set_trace()

FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

class TestMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_trigger_regex_matches(self):

        ## FIXXME: do not only check match/non-match but also number of matching elements:
        
        ## normal org-depend lines:
        self.assertTrue(org-depend_to_org-edna.get_trigger_matches(':TRIGGER:    2016-11-04-some-title(DONE)')
        self.assertTrue(org-depend_to_org-edna.get_trigger_matches(':TRIGGER: 2016-11-04-some-title(DONE)')
        self.assertTrue(org-depend_to_org-edna.get_trigger_matches(':TRIGGER: 2016-11-04-some-title(DONE)  2020-09-19-foo(STARTED)')

        ## org-depend lines that are not "active":
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches(': :TRIGGER:    2016-11-04-some-title(DONE)')
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches('.:TRIGGER: 2016-11-04-some-title(DONE)')
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches(':noTRIGGER: 2016-11-04-some-title(DONE)  2020-09-19-foo(STARTED)')

        ## org-edna lines
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches(':TRIGGER: ids(2020-07-09-new-heading-5) todo!(NEXT) scheduled!(".") ids(2020-07-09-new-heading-6) todo!(NEXT) scheduled!("++2d")')
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches(':TRIGGER:  ids(GProj-Celebrate-and-close-project) todo!(NEXT) scheduled!(".")')
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches(':TRIGGER: ids(taskD) scheduled!(".") todo!(WAITING)')
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches(':TRIGGER: ids(2020-07-11-org-super-links) scheduled!(".")')

        ## org-edna lines that are not "active":
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches(': :TRIGGER: ids(2020-09-19-foo-bar) todo!(NEXT)')
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches(':noTRIGGER: ids(2020-09-19-foo-bar) todo!(NEXT)')
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches('#:TRIGGER: ids(2020-09-19-foo-bar) todo!(NEXT)')
        self.assertFalse(org-depend_to_org-edna.get_trigger_matches('.:TRIGGER: ids(2020-09-19-foo-bar) todo!(NEXT)')
                        
    def test_blocker_regex_matches(self):

        ## FIXXME: do not only check match/non-match but also number of matching elements:

        ## normal org-depend lines:
        self.assertTrue(org-depend_to_org-edna.get_blocker_matches(':BLOCKER:    2016-11-04-some-title')
        self.assertTrue(org-depend_to_org-edna.get_blocker_matches('   :BLOCKER:    2016-11-04-some-title')
        self.assertTrue(org-depend_to_org-edna.get_blocker_matches(':BLOCKER: 2016-11-04-some-title  ')
        self.assertTrue(org-depend_to_org-edna.get_blocker_matches(' :BLOCKER: 2016-11-04-some-title  2020-09-19-foo')
        self.assertTrue(org-depend_to_org-edna.get_blocker_matches(':BLOCKER: 2016-11-04-some-title, 2020-09-19-foo')
        self.assertTrue(org-depend_to_org-edna.get_blocker_matches(':BLOCKER: 2016-11-04-some-title,  2020-09-19-foo')

        ## org-depend lines that are not "active":
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches(': :BLOCKER: 2016-11-04-some-title')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches('#+:BLOCKER: 2016-11-04-some-title')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches(':noBLOCKER: 2016-11-04-some-title')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches('#COMMENT# :BLOCKER: 2016-11-04-some-title')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches('. :BLOCKER: 2016-11-04-some-title')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches('- :BLOCKER: 2016-11-04-some-title')

        ## org-edna lines
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches(':BLOCKER: ids(2020-09-19-foo-bar)')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches(':BLOCKER:     ids(2020-09-19-foo-bar)')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches(' :BLOCKER: ids(2020-09-19-foo-bar)')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches('   :BLOCKER:     ids(2020-09-19-foo-bar)')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches(':BLOCKER:  ids(2020-09-19-foo-bar 2020-09-19-baz)')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches(':BLOCKER:  ids(2020-09-19-foo-bar  2020-09-19-baz)')

        ## org-edna lines that are not "active":
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches(': :BLOCKER: ids(2020-09-19-foo-bar)')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches(':noBLOCKER: ids(2020-09-19-foo-bar)')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches('#:BLOCKER: ids(2020-09-19-foo-bar)')
        self.assertFalse(org-depend_to_org-edna.get_blocker_matches('.:BLOCKER: ids(2020-09-19-foo-bar)')
    
    def test_simple_trigger_line(self):

        self.assertEqual(org-depend_to_org-edna.convert_trigger_line(':TRIGGER:    2016-11-04-some-title(DONE)'),
                         ':TRIGGER: ids(2016-11-04-some-title) todo!(DONE)'
                         )

    def test_trigger_line_with_elisp_snippet(self):

        self.assertEqual(org-depend_to_org-edna.convert_trigger_line(':TRIGGER: prefix-`(my-capture-insert \'my-1)`-notes(STARTED)    prefix2-`(my-capture-insert \'my-foo)`-bar(NEXT)'),
                         ':TRIGGER: ids(prefix-`(my-capture-insert \'my-1)`-notes) todo!(STARTED) ids(prefix2-`(my-capture-insert \'my-foo)`-bar) todo!(NEXT)'
                         )

    def test_simple_blocker_line(self):

        self.assertEqual(org-depend_to_org-edna.convert_trigger_line(':BLOCKER: 2015-07-19-an-id'),
                         ':BLOCKER: ids(2015-07-19-an-id)'
                         )

    def test_blocker_2_ids(self):

        self.assertEqual(org-depend_to_org-edna.convert_trigger_line(':BLOCKER: 2015-07-19-an-id 2020-09-19-another'),
                         ':BLOCKER: ids(2015-07-19-an-id 2020-09-19-another)'
                         )
        
    def test_blocker_2_ids_with_colons(self):

        self.assertEqual(org-depend_to_org-edna.convert_trigger_line(':BLOCKER: 2015-07-19-an-id, 2020-09-19-another'),
                         ':BLOCKER: ids(2015-07-19-an-id 2020-09-19-another)'
                         )
        
        
#        self.assertEqual(org-depend_to_org-edna.convert_trigger_line(''),
#                         ''
#                         )


if __name__ == '__main__':
    unittest.main()
