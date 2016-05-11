import sys
import os, os.path

from mako.template import Template
from mako.lookup import TemplateLookup

'''
	Creates new MAKO template
'''
def create_template(filename):
	file_dir = os.path.dirname(os.path.abspath(__file__))
	template_lookup = TemplateLookup(directories = file_dir,
			input_encoding='utf-8',
			output_encoding='utf-8',
			default_filters=['decode.utf8'])
	print file_dir
	template = Template(
				filename = file_dir + os.sep + filename + ".mako",
				lookup = template_lookup,
				input_encoding='utf-8',
				output_encoding='utf-8',
				default_filters=['decode.utf8'])
	print template.filename
	return template