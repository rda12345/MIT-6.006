#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A file containing simple tests for debugging purposes.
"""

import unittest
import os

if os.environ.get('SOLUTION'):
  from big_num_full import *
else:
  from big_num import *
  

def test_multiplication():
    #print(BigNum.zero() * BigNum.zero() == BigNum.zero())
    print(BigNum.one() * BigNum.one() == BigNum.one())
    print(BigNum.h('1234') * BigNum.h('5678') == BigNum.h('06260060'))
    print(BigNum.h('1234') * BigNum.h('56789A')==
                     BigNum.h('06260B5348'))
    
    print(BigNum.h('FFFFFF') * BigNum.h('FFFFFF') == BigNum.h('FFFFFE000001'))
    print(BigNum.h('FEFDFC') * BigNum.h('FBFAF9F8') == BigNum.h('FAFD0318282820'))


def test_division():
    print(BigNum.one() // BigNum.one() == BigNum.one())
    print(BigNum.zero() // BigNum.one() == BigNum.zero())
    print((BigNum.h('42') // BigNum.h('03') == BigNum.h('16')))
     
    print((BigNum.h('43') // BigNum.h('03') == BigNum.h('16')))
    print(BigNum.h('06260060') // BigNum.h('1234') == BigNum.h('5678'))
    print(BigNum.h('06263F29') // BigNum.h('5678') == BigNum.h('1234'))
    print(BigNum.h('06260FE3C9') // BigNum.h('56789A')==
                     BigNum.h('1234'))
    print(BigNum.h('FFFFFE000001') // BigNum.h('FFFFFF') ==
                     BigNum.h('FFFFFF'))
    print(BigNum.h('FFFFFE0CFEDC') // BigNum.h('FFFFFF') ==
                     BigNum.h('FFFFFF'))
    print(BigNum.h('FAFD0318282820') // BigNum.h('FEFDFC') ==
                     BigNum.h('FBFAF9F8'))
    print(BigNum.h('FAFD0318C3D9EF') // BigNum.h('FEFDFC') ==
                     BigNum.h('FBFAF9F8'))
    print(BigNum.h('100000000') // BigNum.h('20000') ==
                     BigNum.h('8000'))


def test_slow_multiplication():
    old_mul = BigNum.__mul__
    try:
      print('check ')
      BigNum.__mul__ = BigNum.slow_mul
      test_multiplication()
    finally:
      print('finish')
      BigNum.__mul__ = old_mul
      
      
def test_slow_division():
    old_divmod = BigNum.__divmod__
    try:
      print('check ')
      BigNum.__divmod__ = BigNum.slow_divmod
      test_division()
    finally:
      print('finish')
      BigNum.__divmod__ = old_divmod
      
    
    
#test_slow_multiplication()
test_slow_division()

