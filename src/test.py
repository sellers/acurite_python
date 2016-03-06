import requests
from datetime import datetime as dt
import json
from subprocess import Popen, PIPE
import sys
user = 'KMISALIN2'
pw = 'SalineWeather'
baseurl = "http://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?"
#http://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?ID=KCASANFR5
#&PASSWORD=XXXXXX&dateutc=2000-01-01+10%3A32%3A35&winddir=230&windspeedmph=12
#&windgustmph=12&tempf=70&rainin=0&baromin=29.1&dewptf=68.2&humidity=90&weather=
#&clouds=&softwaretype=vws%20versionxx&action=updateraw&realtime=1&rtfreq=2.5
# {"windSpeed":{"WS":"3.1","t":"1457194197"},"windDirection":{"WD":"E","t":"1457194187"},
#"temperature":{"T":"32.0","t":"1457194197"},"humidity":{"H":"90","t":"1457194197"},
#"rainCounter":{"RC":"32","t":"1457194187"}}


def wunder(data, now):

    url = ("{}&ID={}&PASSWORD={}&dateutc={}&winddir={}&windspeedmph={}&windgustmph={}"
           "&tempf={}&rainin={}&baromin={}&softwaretpye=sellers.py"
           .format(baseurl, user, pw, now, data['windDirection["WD"]'],
                   data['windSpeed["WS"]'],
                   '',
                   data['temperature["T"]'],
                   data['rainCounter["RC"]'],
                   ''))
    print('sending to {}'.format(url))
    resp = requests.put(url)
    print(resp.text)
    print(resp.status)


def read():
    now = dt.now().strftime('%Y-%m-%d+%H:%M:%S')
    with Popen('/usr/local/bin/wstation', stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True) as p:
        while True:
            data = p.stdout.readline()
            if len(data) == 0:
                break
            sys.stdout.write(data)
            jdata = json.dumps(data)
            wunder(jdata, now)

if __name__ == "__main__":
    read()
