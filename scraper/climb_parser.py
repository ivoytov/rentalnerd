from bs4 import BeautifulSoup
import csv
from re import sub
from decimal import Decimal
import time

rented = open('rented.html')

soup = BeautifulSoup(rented, 'html.parser')
all_listings = []

print len(soup.find_all('div', class_="properties-list-details"))


for listing in soup.find_all('div', class_="properties-list-details"):
	
	# the address is usually the first 'p' tag. If building lacks name, address is in 'h4'
	address = listing.contents[1].text

	if  address == "":
		address = listing.contents[0].text

	# neighborhood is stored in this way. We only save what's in the ()
	# 'San Francisco (SOMA)' or East Bay (Oakland)
	neighborhood = listing.contents[2].text.split('(')[1][:-1]

	# next line has number of bedrooms, bathrooms, and house type:
	# '1 BR, 1 BA Condo' or '4 BR, 3.5 BA Single-Family'
	line = listing.contents[3].text.split(',')
	bedrooms = line[0].split()[0]
	if bedrooms == 'Studio':
		bedrooms = 0
	elif bedrooms == 'Jr':
		bedrooms = 0

	bedrooms = int(bedrooms)
	bathrooms = float(line[1].split()[0])

	# next line shows the final rent. Except some listings don't show the price.
	# Rented $2,975
	try:
		price = Decimal(sub(r'[^\d.]', '', listing.contents[4].text.split('$')[1]))
	except IndexError:
		# no rent amount is listed. ignore the listing, proceed to next listing
		continue

	# next line shows date lease was signed
	# Rented on 06/15/2015
	date = listing.contents[5].text.split()[2]


	new_listing = {
		'Address': address,
		'Neighborhood': neighborhood,
		'Bedrooms': bedrooms,
		'Bathrooms': bathrooms,
		'Price': price,
		'Rented': True,
		# 'Rented': False,
		'Date': date,
		'Source': 'Climb SF'
	}
	print new_listing
	all_listings.append(new_listing)


with open('climb_listings_active_dates.csv', 'w') as csvfile:
	fieldnames = [
		'Address',
		'Neighborhood',
		'Bedrooms',
		'Bathrooms',
		'Price',
		'Rented',
		'Date',
		'Source'
	]

	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
	writer.writeheader()
	writer.writerows(all_listings)
