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
from weather import get_weather

# the names and websites of each food menu
places = [('Commons',
           'http://www.uvic.ca/services/food/what/cadboromenu/index.php'),
          ('Centre',
           'http://www.uvic.ca/services/food/what/centremenu/index.php'),
          ('VGs',
           'http://www.uvic.ca/services/food/what/villagegreensmenu/index.php')]

# Map numeric day of week, to english name
day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

#what day of the week is it?  Make 0-4 Monday - Friday
day = date.today().isoweekday() - 1

#if we are run on a weekend, just exit
if not 0 <= day <= 5:
    sys.exit(0)

# the lunch text
lunch = []

#the subject line of the email
titles = []

# open the url, parse, then pull out lunch info
for place in places:
    soup = BeautifulSoup(urllib2.urlopen(place[1]).read(),
                         convertEntities=BeautifulSoup.HTML_ENTITIES)
    # get all the id=lunch elements
    days = soup('div', {'id': 'lunch'})
    # pick the one for this day of the week
    lunch.append(day_of_week[day] + " at " + place[0])

    try:
        row = days[day]
    except:
        lunch.append("Closed.\n")

        continue

    # now get the actual text
    for i in xrange(0, len(row('h4'))):
        lunch.append(row('h4')[i].string)
        titles.append(row('h4')[i].string)
        lunch.append(row('p')[i].string + "\n")
    

    lunch.append("")

# get lunch weather
forecast = get_weather()
# if we found a lunch forecast, add it
if forecast:
    lunch.append("UVic Lunchtime Weather:\n")
    lunch.extend(forecast)


def send_to(email_addr, subject, body ):

    # now email the results!
    import smtplib
    fromaddr = 'chris4000@gmail.com'
    toaddrs  = email_addr
    msg = """From: %s
To: %s
Bcc: %s
Subject: %s

%s
"""% ("Auto-lunch", toaddrs, fromaddr, ', '.join(subject), '\n'.join(body))
    
    # Credentials (if needed)
    creds = open("/home/cmatthew/credentials", 'r')
    username = creds.readline()[:-1]  # munis the newline
    password = creds.readline()[:-1]  # minus the newline

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.encode("utf-8"))
    server.quit()


send_to("chris4000@gmail.com", titles, lunch)
send_to("uvic-lunch@googlegroups.com", titles, lunch)
