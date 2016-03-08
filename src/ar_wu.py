#!/usr/bin/python3
"""
Collect data from acurite station and send it to weather underground.

This leverages the weatherstation.c code from
It will run over and over reading data from the USB port set to #4 on the dev
"""

import json
from time import sleep
import argparse
import requests
import configparser
from subprocess import Popen, PIPE
from datetime import datetime as dt


class wunder(object):

    """
    Read from weatherstation app and push to wunderground.

    kdfjkd
    """

    def __init__(self,
                 config=None,
                 user=None,
                 pw=None,
                 cmd='/usr/local/bin/wstation'):
        """start the class."""
        self.config = config
        self.baseurl = ('http://rtupdate.wunderground.com/weatherstation/'
                        'updateweatherstation.php?')
        self.user = user
        self.pw = pw
        self.cmd = cmd

    def read_config(self):
        """read the configuration."""
        config = configparser.ConfigParser()
        config.read(self.config)
        self.user = config['DEFAULT']['user']
        self.pw = config['DEFAULT']['pass']

    def wunder(self, data):
        """send wundergrounad the data."""
        now = dt.now().strftime('%Y-%m-%d+%H:%M:%S')
        url = ''
        sleep(120)
        if data['windDirection']['WD'] != "":
            url = ("{}&winddir={}".format(url, data['windDirection']['WD']))
        if float(data['windSpeed']['WS']) > 0:
            url = ("{}&windspeedmph{}".format(url, data['windSpeed']['WS']))
        if float(data['temperature']['T']) > 0:
            url = ("{}&tempf={}".format(url, data['temperature']['T']))
        if float(data['barometer']['B']) > 0:
            url = ("{}&baromin={}".format(url, data['barometer']['B']))
        if float(data['humidity']['H']) > 0:
            url = ("{}&humidity={}".format(url, data['humidity']['H']))
        if float(data['rainCounter']['RC']) > 0:
            url = ("{}&rainin={}".format(url, data['rainCounter']['RC']))

        url = ('{}&ID={}&PASSWORD={}&dateutc={}'
               '{}&softwaretype=ar_wu.py&realtime=1&rtfreq=2&action=update_rw'
               .format(self.baseurl,
                       self.user,
                       self.pw,
                       now,
                       url))
        #('{}&ID={}&PASSWORD={}&dateutc={}&winddir={}'
        #       '&windspeedmph={}&windgustmph={}&humidity={}'
        #       '&tempf={}&rainin={}&baromin={}&softwaretype=sellers.py'
        #       '&realtime=1&rtfreq=2.5&action=update_raw'
        #       .format(self.baseurl,
        #               self.user,
        #               self.pw,
        #               now,
        #               data['windDirection']['WD'],
        #               data['windSpeed']['WS'],
        #               '',
        #               data['humidity']['H'],
        #               data['temperature']['T'],
        #               data['rainCounter']['RC'],
        #               ''))
        print(url)
        requests.get(url)
        print(requests)

    def read_usb(self):
        """read the usb."""
        try:
            print('Readn the usb: {}'.format(self.cmd))
            with Popen(self.cmd,
                       stdout=PIPE,
                       stderr=PIPE,
                       bufsize=1,
                       universal_newlines=True) as p:
                while True:
                    data = p.stdout.readline()
                    if len(data) == 0:
                        break
                    jdata = json.loads(data)
                    self.wunder(jdata)
        except Exception as po_py:
            print("USB Read Err {}".format(po_py))


def parser():
    """
    Parse args pass in if not used as library/module.

    returns: an argparse object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Debug output')
    parser.add_argument('-w',
                        '--wunderground',
                        action='store_true',
                        help='share with wundergroun')
    parser.add_argument('-c',
                        '--config',
                        default='/usr/local/etc/w.conf')
    parser.add_argument('-u',
                        '--stationid',
                        default=None,
                        help='WU Station ID')
    parser.add_argument('-p',
                        '--passwd',
                        default=None,
                        help='WU account password')
    parser.add_argument('-r',
                        '--cmd',
                        default='/usr/local/bin/wstation',
                        help='wstation command+path')
    return parser.parse_args()


def main():
    """Invoked from CLI."""
    print("Start me up!\n\n")
    ARGS = parser()
    WUND = wunder(config=ARGS.config,
                  user=ARGS.stationid,
                  pw=ARGS.passwd,
                  cmd=ARGS.cmd)
    if ARGS.config:
        WUND.read_config()
        if ARGS.debug:
            print(ARGS.config)
    if ARGS.wunderground:
        WUND.read_usb()


if __name__ == '__main__':
    print('main')
    main()
print('goodbye {}.'.format(__name__))
