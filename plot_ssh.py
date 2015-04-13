import argparse
import json
import re
import requests
from iptools.ipv4 import validate_ip


# IPADDRESS_PATTERN = "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
# pattern = pattern.compile(IPADDRESS_PATTERN)
check = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"


def get_ip_location(ip):
    '''
    The Geo location for the IP is grabbed from the freegeoip service (
    https://freegeoip.net/) running on localhost
    '''
    response = requests.get('http://127.0.0.1:8080/json/{ip}'.format(ip=ip))
    response.raise_for_status()
    return response


def plot_ssh(args):
    '''
    Parse the SSH log file and locate where hack attempts originate from
    '''
    with open(args.ssh_log, 'rU') as ssh_log:
        for line in ssh_log.xreadlines():
            m = re.findall(check, line)
            # if line.find('User root from') >= 0:
            #     import pdb;pdb.set_trace()
            if any(m):
                ip = m[0]
                print ip
                if validate_ip(ip):
                    location = json.loads(get_ip_location(ip))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ssh_log', help='Absolute path to the system SSH log')
    args = parser.parse_args()

    plot_ssh(args)
