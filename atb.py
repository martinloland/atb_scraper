import requests
from bs4 import BeautifulSoup as soup

payload ={'lang':'no', 'from':'Odenseveien (Trondheim)', 'to':'Sentrum (Trondheim)'}
link = 'https://rp.atb.no/scripts/TravelMagic/TravelMagicWE.dll/svar'
r = requests.get(link, params=payload)

if r.status_code is 200:
	soup = soup(r.content, 'html.parser')
	planlagte_tider = soup.findAll('span', {'class':'tm-rf-planlagt'})[:3]
	nye_tider = soup.findAll('span', {'class':'tm-rf-nytid'})[:3]
	busser = soup.findAll('span', {'class':'tm-det-linenr'})[:3]

	print('\nOdenseveien, mot sentrum\n')
	print('{:10}{:10}{:10}\n{}'.format('Avgang', 'Ny tid','Buss','-'*25))

	for plan, ny, buss in zip(planlagte_tider, nye_tider, busser):
		print('{:10}{:10}{:10}'.format(plan.text, ny.text, buss.text))
	print('\n')
else:
	raise UserWarning('Error making request, status code: {}'.format(r.status_code))