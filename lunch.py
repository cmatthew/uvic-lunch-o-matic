import urllib2
import sys
from datetime import date
from BeautifulSoup import BeautifulSoup

places = [('Commons','http://www.uvic.ca/services/food/what/cadboromenu/index.php'),
          ('Centre','http://www.uvic.ca/services/food/what/centremenu/index.php'),
          ('VGs','http://www.uvic.ca/services/food/what/villagegreensmenu/index.php')]
day_of_week = ['Monday','Tuesday','Wednesday','Thursday','Friday']

#what day of the week is it?  Make 0-4 Monday - Friday
day = date.today().isoweekday() -1

#if we are run on a weekend, just exit
if not 0 <= day <= 5:
    sys.exit(0)

# the lunch text
lunch = []

#the subject line of the email
titles = []

for place in places:
    soup = BeautifulSoup(urllib2.urlopen(place[1]).read())
    # get all the id=lunch elements
    days =  soup('div', {'id' : 'lunch'})
    # pick the one for this day of the week
    row = days[day]
    lunch.append( day_of_week[day] + " at " + place[0])

    # now get the actual text
    for i in xrange(0,len(row('h4'))):
        lunch.append( row('h4')[i].string)
        titles.append( row('h4')[i].string)
        lunch.append( row('p')[i].string + "\n")
    lunch.append("")

# now email the results!
import smtplib
fromaddr = 'chris4000@gmail.com'
#toaddrs  = 'chris4000@gmail.com'
toaddrs  = 'uvic-lunch@googlegroups.com'
msg = """\
From: %s
To: %s
Subject: %s

%s
""" % ("Auto-lunch", toaddrs, ', '.join(titles), '\n'.join(lunch))

msg = msg.replace("&amp;","&")

# Credentials (if needed)
creds = open("credentials",'r')
username = creds.readline()[:-1] # munis the newline
password = creds.readline()[:-1] # minus the newline

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg.encode("utf-8"))
server.quit()  
