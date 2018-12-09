# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "man", "--nolog"])
# while True:
#     import base64
#     lines = open('./test1.html', 'r').readlines()
#     lines1 = open('./test.html.bak', 'r').readlines()
#     for i in range(len(lines)):
#         b1 = base64.encodestring(lines[i])
#         b2 = base64.encodestring(lines1[i])
#         print(b1, b2, b1 == b2)
#     execute(["scrapy", "crawl", "man", "--nolog"])
#     sys.exit(1)
#     time.sleep(60)
    