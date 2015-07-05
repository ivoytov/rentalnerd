import requests
from bs4 import BeautifulSoup

url = 'http://www.climbsf.com/wp-content/themes/realestate/'
api = 'rent-ajaxproperty-brick.php'

# code for rented: 3 is for rent, 4 is rented
payload = {'price': '', 'beds': '', 'baths': '', 'region': 'All', 'rented': 4 }
r = requests.get(url + api, params=payload)

rented = open('rented.html', 'w')
rented.write(r.text)

soup = BeautifulSoup(r.text, 'html.parser')

print 'Scraped ' + `len(soup.find_all('div'))` + ' rented listings'