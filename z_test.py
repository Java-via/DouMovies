# _*_ coding: utf-8 _*_

import pybloom

bf = pybloom.BloomFilter(capacity=100000000, error_rate=0.001)
bf.add("test")

