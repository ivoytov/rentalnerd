import requests
from bs4 import BeautifulSoup
import csv

url = 'http://www.climbsf.com/wp-content/themes/realestate/'
api = 'rent-ajaxproperty-brick.php'

# code for rented: 3 is for rent, 4 is rented
# get rented units
payload = {'price': '', 'beds': '', 'baths': '', 'region': 'All', 'rented': 4 }
r = requests.get(url + api, params=payload)

# get active listings
payload = {'price': '', 'beds': '', 'baths': '', 'region': 'All', 'rented': 3 }
l = requests.get(url + api, params=payload)

rented = open('rented.html', 'w')
rented.write(r.text)

listings = open('listings.html','w')
listings.write(l.text)

soup = BeautifulSoup(r.text, 'html.parser')

print 'Scraped ' + `len(soup.find_all('div'))` + ' rented listings'

for listing in soup.find_all('a'):
	print listing.href