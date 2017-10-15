import requests
from datetime import datetime, timezone, timedelta


def remaining_minutes(bus_time, now):
    h = int(bus_time.split(':')[0])
    m = int(bus_time.split(':')[1])
    arrival = now.replace(hour=h, minute=m)
    remaining = arrival-now
    remaining_min = int(remaining.total_seconds()/60)
    return remaining_min


def arrival_time(planned_time, new_time):
    if new_time.rstrip() != '':
        return new_time.rstrip()
    else:
        return planned_time.rstrip()


def get_departues(rows):
    from bs4 import BeautifulSoup as soup
    if rows > 10:
        raise ValueError('Can not handle more than 10 rows')
    results = []
    SUCCESSFUL_REQUEST_CODE = 200

    payload ={'from':'Odenseveien (Trondheim)', 'to':'Sentrum (Trondheim)'}
    link = 'https://rp.atb.no/scripts/TravelMagic/TravelMagicWE.dll/svar'
    r = requests.get(link, params=payload)

    now = datetime.now()

    if r.status_code is SUCCESSFUL_REQUEST_CODE:
        soup = soup(r.content, 'html.parser')
        planned_times = soup.findAll('span', {'class':'tm-rf-planlagt'})[::2]
        new_times = soup.findAll('span', {'class':'tm-rf-nytid'})[::2]
        busses = soup.findAll('span', {'class':'tm-det-linenr'})


        for planned, new, bus in zip(planned_times[:rows], new_times[:rows], busses[:rows]):
            arrival = arrival_time(planned.text, new.text)
            remaining = remaining_minutes(arrival, now)
            if remaining <= 15:
                arrival = '{} min'.format(remaining)
            results.append({'bus':bus.text.rstrip(), 'arrival':arrival})
    else:
        raise UserWarning('Error making request, status code: {}'.format(r.status_code))

    return results



# ROWS = 3
# SUCCESSFUL_REQUEST_CODE = 200
#
# payload ={'from':'Odenseveien (Trondheim)', 'to':'Sentrum (Trondheim)'}
# link = 'https://rp.atb.no/scripts/TravelMagic/TravelMagicWE.dll/svar'
# r = requests.get(link, params=payload)
#
# delta = timedelta(seconds=60*60*2) #Two hours
# now = datetime.now(timezone.utc)+delta
#
# if r.status_code is SUCCESSFUL_REQUEST_CODE:
#     soup = soup(r.content, 'html.parser')
#     planlagte_tider = soup.findAll('span', {'class':'tm-rf-planlagt'})[::2]
#     nye_tider = soup.findAll('span', {'class':'tm-rf-nytid'})[::2]
#     busser = soup.findAll('span', {'class':'tm-det-linenr'})
#
#     print('\nOdenseveien, mot sentrum\n\n{:>5}{:>10}\n{}'.format('Rute', 'Avgang','-'*15))
#
#     for plan, ny, buss in zip(planlagte_tider[:ROWS], nye_tider[:ROWS], busser[:ROWS]):
#         arrival = arrival_time(plan.text, ny.text)
#         remaining = remaining_minutes(arrival)
#         if remaining <= 15:
#             arrival = '{} min'.format(remaining)
#         print('{:>5}{:>10}'.format(buss.text.rstrip(), arrival))
#     print('\n')
# else:
#     raise UserWarning('Error making request, status code: {}'.format(r.status_code))