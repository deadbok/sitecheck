# coding=utf-8
'''
Created on 06/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: GPLv3, see LICENSE for more details.
'''
from subprocess import Popen, PIPE
import os.path
import shlex


def get_simple_cmd_output(cmd):
    """
    Execute an external command and get its output.
    """
    # Split the command and arguments
    args = shlex.split(cmd)
    # Return everything from stdout
    ret = Popen(args, stdout=PIPE)
    # Convert to string
    ret_out = ret.communicate()[0].decode(encoding)
    # Return code
    ret = ret.returncode

    return(ret, ret_out)



def diff_index_page(host):
	"""
	Diff /index.html of the host with last copy.
	"""
	host = host.strip()
	print("Getting index.html from: " + host)
	# ping command
	cmd = "curl -s -L " + host.strip()
	# Run
	res = get_simple_cmd_output(cmd)

	index_file_name = "sites/" + host + "-index.html"
	# Rename the old one if it is there
	if os.path.isfile(index_file_name):
		os.rename(index_file_name, index_file_name + ".old")

	# Save new index.html
	index_file = open(index_file_name, "w");
	if index_file is not None:
		index_file.write(res[1])
		index_file.close()
	else:
		print("Could not write: " + index_file_name);

	if os.path.isfile(index_file_name + ".old"):
		print("Diffing: " + index_file_name)
		# diff command
		cmd = "diff -u1 " + index_file_name + ".old " + index_file_name
		# Run
		res = get_simple_cmd_output(cmd)

		# old_index_file = open(index_file_name, "r");
		# old_index = old_index_file.read()
		# index_file = open(index_file_name, "r");
		# index = index_file.read()
		# Eeeeew
		# diff = difflib.unified_diff(old_index, index, fromfile=index_file_name + ".old", tofile=index_file_name)
		return(res[1])

	return("No old index");
