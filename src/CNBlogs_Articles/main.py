import sys
import os

from scrapy.cmdline import execute
print(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","cnblogs"])

