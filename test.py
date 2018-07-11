#!/usr/bin/python3

import sys
import re
import unittest
from patterns import (
    build_regex_pattern,
    path_match,
    best_patterns
)

class PatternsTestCase(unittest.TestCase):
    def setUp(self):
        self.re_pattern_1 = build_regex_pattern('*')
        self.re_pattern_2 = build_regex_pattern('Wa8', case=True)
        self.re_pattern_3 = build_regex_pattern('hd+')
        self.re_pattern_4 = build_regex_pattern('cl*dn')
        self.patt = ['*', '*', 'hbo', '*']
        self.path = ['7&kQ', 'hd', 'HBO', 'aabc!']
        self.patt1 = '*,*,hBo,*,tra,*'
        self.patt2 = '*,U,*,zp,*jgQ,*'
        self.patt3 = '*,*,*,n,*L,*'
        self.patt4 = 'g,h,t,*,*,*'
        self.patt5 = '*,h,6,pf,x,*'
        self.patt6 = ['*', 'hd', 'hbo', '*']
        self.patt7 = 'st,tu*fdj,vl$,*,*' #In case '*' appears within a pattern's field
        self.patt8 = '*,gh,best,*,end'
        self.result1 = best_patterns(self.patt1, self.patt2)
        self.result2 = best_patterns(self.patt2, self.patt3)
        self.result3 = best_patterns(self.patt4, self.patt5)
        self.result4 = best_patterns(self.patt7, self.patt8)


    def test_build_re_pattern(self):
        self.assertTrue(self.re_pattern_1.match('%*3Y_-/5 H)'))
        self.assertFalse(self.re_pattern_1.match('géh^\e'))
        self.assertTrue(self.re_pattern_2.match('wA8'))
        self.assertTrue(self.re_pattern_3.match('hd+'))
        self.assertTrue(self.re_pattern_4.match('cl*dn'))

    def test_path_match(self):
        self.assertTrue(path_match(self.patt6, self.path, case=True))
        self.assertFalse(path_match(self.patt1, self.path, case=True))
        self.assertFalse(path_match(self.patt, self.path, case=False))

    def test_best_patterns(self):
        self.assertEqual(self.result1, self.patt2)
        self.assertEqual(self.result2, self.patt2)
        self.assertEqual(self.result3, self.patt5)
        self.assertEqual(self.result4, self.patt7)


if __name__ == '__main__':
    unittest.main()
