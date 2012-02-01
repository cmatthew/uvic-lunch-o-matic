import urllib2
import sys
from datetime import date
from BeautifulSoup import BeautifulSoup


def get_weather():

    soup = BeautifulSoup(
        urllib2.urlopen("http://www.theweathernetwork.com/hourlyfx/cabc0256\
        /hourlytable/1/?ref=tabs_hourly_table").read())

    hour_table = soup.findAll('td', attrs={'class': 'hour'})
    cond_table = soup.findAll('td', attrs={'class': 'cond'})

    results = []

    for i in xrange(0, len(hour_table)):
        if  hour_table[i].string in ["11am", "12pm", "1pm"]:
            results.append(hour_table[i].string + " " + cond_table[i].string)

    return results
