import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime, timezone, timedelta, date, time
from time import gmtime, strftime

payload ={'lang':'no', 'from':'Odenseveien (Trondheim)', 'to':'Sentrum (Trondheim)'}
link = 'https://rp.atb.no/scripts/TravelMagic/TravelMagicWE.dll/svar'
r = requests.get(link, params=payload)

delta = timedelta(seconds=60*60*2) #Two hours
now = datetime.now(timezone.utc)+delta

if r.status_code is 200:
	soup = soup(r.content, 'html.parser')
	planlagte_tider = soup.findAll('span', {'class':'tm-rf-planlagt'})[:3]
	nye_tider = soup.findAll('span', {'class':'tm-rf-nytid'})[:3]
	busser = soup.findAll('span', {'class':'tm-det-linenr'})[:3]

	print('\nOdenseveien, mot sentrum\n')
	print('{:10}{:5}\n{}'.format('Avgang', 'Buss','-'*15))

	for plan, ny, buss in zip(planlagte_tider, nye_tider, busser):
		if ny.text.rstrip() != '':
			bus_time = ny.text.rstrip()
		else:
			bus_time = plan.text.rstrip()
		h = int(bus_time.split(':')[0])
		m = int(bus_time.split(':')[1])
		arrival = now.replace(hour=h, minute=m)
		remaining = arrival-now
		remaining_min = int(remaining.total_seconds()/60)
		if remaining_min <= 15:
			bus_time = '{} min'.format(remaining_min)

		print('{:>8}{:>5}'.format(bus_time, buss.text.rstrip()))
	print('\n')
else:
	raise UserWarning('Error making request, status code: {}'.format(r.status_code))