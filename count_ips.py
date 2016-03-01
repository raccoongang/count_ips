""" 
Module destinated for determining a count of users, who visited site in specified time
    from nginx logs.

You must specify args:
    -f - file (gz format)
    -to - to time HH:MM
    -from - time from HH:MM
    --show-ip - shows list of ips

Example of usage:
    
    python count_ips.py -f <filename.gz> -from 12:00 -to 19:00 --show-ip

    or

    python count_ips.py -f <filename.gz>

"""

import sys
import re
import gzip
import datetime


args = sys.argv
time_from = datetime.time(0, 0)
to_time = datetime.time(23, 59, 59)
ip_list = []
EXCEPTED_IPS = (
    '127.0.0.1', # localhost 
    '82.117.232.99' # our ip
    )

template_for_time = '(?<=:)\d{2}\:\d{2}'
template_for_ip = '\d+\.\d+\.\d+\.\d+'

flag_from = flag_to = False

if len(args) == 1 or '--help' in args:
	print __doc__
	sys.exit()

try:
    input_file = args[args.index('-f') + 1]
except:
	print 'You must specify filename'
	sys.exit()

try:
    arg_time_from = args[args.index('-from') + 1].split(':')[:2]
    time_from = datetime.time(int(arg_time_from[0]), int(arg_time_from[-1]))
    flag_from = True
except:
    pass

try:
    arg_to_time = args[args.index('-to') + 1].split(':')[:2]
    to_time = datetime.time(int(arg_to_time[0]), int(arg_to_time[-1]))
    flag_for = True
except:
    pass


def check_time(row, t_from, t_to):
    search_result = re.search(template_for_time, row).group().split(':')
    time_res = datetime.time(int(search_result[0]), int(search_result[-1]))
        
    return t_from < time_res < t_to
    

search = lambda template: re.search(template_for_ip, template).group()


with gzip.open(input_file) as file:
    lines = file.readlines()
    for row in lines:
        if not search(row) in ip_list and search(row) not in EXCEPTED_IPS and check_time(row, time_from, to_time):
            ip_list.append(search(row))
        else:
            continue


if flag_to or flag_from:
	print time_from, to_time

print 'Count of users: ', len(ip_list)

if '--show-ip' in args:
	print 'Ips:'
	for ip in ip_list:
	    print ip
