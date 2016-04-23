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

# rented = open('rented.html', 'w')
# rented.write(r.text)

# listings = open('listings.html','w')
# listings.write(l.text)

soup = BeautifulSoup(l.text, 'html.parser')

print 'Scraped ' + `len(soup.find_all('div'))` + ' rented listings'

all_listings = []

for link in soup.find_all('a'):
	a = requests.get(link.get('href'))
	print link.get('href')
	link_soup = BeautifulSoup(a.text, 'html.parser')

	listing = {
		'Url': link.get('href'),
		'Sqft': 'NA'
	}
	# print link_soup.find_all('span')
	for text in link_soup.find_all(string='Square Feet:'):
		listing['Sqft'] = text.parent.next_sibling

	all_listings.append(listing)

with open('climb_active_sqft.csv', 'w') as csvfile:


	fieldnames = ['Url', 'Sqft']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
	writer.writeheader()
	writer.writerows(all_listings)
