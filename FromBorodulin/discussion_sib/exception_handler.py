# -*- coding: utf-8 -*-
import sys
import os, os.path

def error_handler(debug_mode = False, e = None):
    if debug_mode and e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return "Exception '{}' in {} on line {}: {} {}".format(type(e).__name__, fname, exc_tb.tb_lineno, str(e), exc_type)
    else:
        return "Unknown error\n"
