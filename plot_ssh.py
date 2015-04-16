import argparse
import json
import re
import requests
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from iptools.ipv4 import validate_ip
from mpl_toolkits.basemap import Basemap


# IPADDRESS_PATTERN = "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
# pattern = pattern.compile(IPADDRESS_PATTERN)
check = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
matplotlib.use('Agg')


def get_ip_location(ip):
    '''
    The Geo location for the IP is grabbed from the freegeoip service (
    https://freegeoip.net/) running on localhost
    '''
    response = requests.get('http://127.0.0.1:8080/json/{ip}'.format(ip=ip))
    response.raise_for_status()
    return response


def plot_ssh(ssh_log, plot_file):
    '''
    Parse the SSH log file and locate where hack attempts originate from
    '''
    ip_map = Basemap(projection='robin', lon_0=0, resolution='c')

    logged_ips = {}
    with open(ssh_log, 'rU') as ssh_log:
        for line in ssh_log.xreadlines():
            if line.find('User root from') >= 0:
                m = re.findall(check, line)
                if any(m):
                    ip = m[0]
                    if validate_ip(ip):
                        if ip not in logged_ips.keys():
                            logged_ips[ip] = 1
                            location = json.loads(get_ip_location(ip).content)
                            x, y = ip_map(location['longitude'], location['latitude'])
                            plt.plot(x,y, 'o', color='#ff0000', ms=2.7, markeredgewidth=0.5)
                        else:
                            logged_ips[ip] += 1

    ip_map.drawcountries(color='#ffffff')
    ip_map.fillcontinents(color='#cccccc',lake_color='#ffffff')

    plt.savefig(plot_file, dpi=600)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ssh_log', help='Absolute path to the system SSH log')
    parser.add_argument(
        'plot_file',
        help='Absolute path to the generated map image',
        default='/var/projects/ssh_hack_plot/hack_plot.png'
    )
    args = parser.parse_args()

    ssh_log = args.ssh_log
    plot_file = args.plot_file

    plot_ssh(ssh_log, plot_file)
