# -*- encoding: utf-8 -*-

from in_multi_in import in_multi_in
from esm_multi_in import esm_multi_in

import re
import unittest


class BaseMultiInTest(object):
                
    def test_simplest(self):
        in_list = ['123','456','789']
        imi = self.klass( in_list )

        result = imi.query( '456' )
        self.assertEqual(1, len(result))
        self.assertEqual('456', result[0])

        result = imi.query( '789' )
        self.assertEqual(1, len(result))
        self.assertEqual('789', result[0])
        
    def test_assoc_obj(self):
        in_list = [ ('123456', None, None) , ('abcdef', 1, 2) ]
        imi = self.klass( in_list )

        result = imi.query( 'spam1234567890eggs' )
        self.assertEqual(1, len(result))
        self.assertEqual('123456', result[0][0])
        self.assertEqual(None, result[0][1])
        self.assertEqual(None, result[0][2])

        result = imi.query( 'foo abcdef bar' )
        self.assertEqual(1, len(result))
        self.assertEqual('abcdef', result[0][0])
        self.assertEqual(1, result[0][1])
        self.assertEqual(2, result[0][2])

    def test_special_char(self):
        in_list = ['javax.naming.NameNotFoundException', '7', '8']
        imi = self.klass( in_list )
        
        result = imi.query( 'abc \\n javax.naming.NameNotFoundException \\n 123' )
        self.assertEqual(1, len(result))
        self.assertEqual('javax.naming.NameNotFoundException', result[0])
        
        in_list = [u'abc(def)', u'foo(bar)']
        imi = self.klass( in_list )
        
        result = imi.query( 'foo abc(def) bar' )
        self.assertEqual(1, len(result))
        self.assertEqual('abc(def)', result[0])
    
    def test_unicode(self):
        in_list = [u'ñ', u'ý']
        imi = self.klass( in_list )
        
        result = imi.query( 'abcn' )
        self.assertEqual(0, len(result))
        
        result = imi.query( 'abcñ' )
        self.assertEqual(1, len(result))
        self.assertEqual('ñ', result[0])

    def test_null_byte(self):
        in_list = ['\x00']
        imi = self.klass( in_list )

        result = imi.query( 'abc\x00def' )
        self.assertEqual(1, len(result))
        self.assertEqual('\x00', result[0])


class TestEsmMultiIn(unittest.TestCase, BaseMultiInTest):
    def __init__(self, testname):
        super(TestEsmMultiIn, self).__init__(testname)
        self.klass = esm_multi_in

class TestInMultiIn(unittest.TestCase, BaseMultiInTest):
    def __init__(self, testname):
        super(TestInMultiIn, self).__init__(testname)
        self.klass = in_multi_in

if __name__ == '__main__':
    unittest.main()