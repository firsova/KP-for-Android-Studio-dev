# -*- coding: utf-8 -*-
import sys
import os, os.path

def error_handler(e = None):
    if e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return "Exception '{}' in {} on line {}: {}".format(type(e).__name__, fname, exc_tb.tb_lineno, str(e))
    else:
        return "Unknown error\n"
