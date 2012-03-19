# Uvic-lunch is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
