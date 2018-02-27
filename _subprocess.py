#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/21 10:43
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : _subprocess.py

# Import the module
import subprocess

# Ask to user for input
host = raw_input('Enter a host to ping:')

# Set up the echo command and direct the output to a pipe
p1 = subprocess.Popen(['ping', '-c 2', host], stdout=subprocess.PIPE)

# Run the command
output = p1.communicate()[0]
print output


def execute_shell_command(command):
    child = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = child.stdout.read()
    child.wait()
    if child.returncode != 0:
        print 'Executing Command {} Error!'.format(command)
        exit(child.returncode)
    return output


print execute_shell_command('ping -c 2 www.baidu.com')