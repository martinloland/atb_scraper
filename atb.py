import requests
from bs4 import BeautifulSoup as soup

payload ={'lang':'no', 'from':'Odenseveien (Trondheim)', 'to':'Sentrum (Trondheim)'}
link = 'https://rp.atb.no/scripts/TravelMagic/TravelMagicWE.dll/svar'
r = requests.get(link, params=payload)

if r.status_code is 200:
	soup = soup(r.content, 'html.parser')
	planlagte_tider = soup.findAll('span', {'class':'tm-rf-planlagt'})[:3]
	nye_tider = soup.findAll('span', {'class':'tm-rf-nytid'})[:3]

	print('Odenseveien, mot sentrum\n')
	print('{:10}{:10}\n{}'.format('Avgang', 'Ny tid','-'*20))

	for plan, ny in zip(planlagte_tider, nye_tider):
		print('{:10}{:10}'.format(plan.text, ny.text))
else:
	raise UserWarning('Error making request, status code: {}'.format(r.status_code))