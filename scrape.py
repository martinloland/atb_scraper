import requests
from datetime import datetime


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

    payload ={
        'dep1':'1',
        'from':'16011351',
        'to':'Sentrum (Trondheim)'
    }
    link = 'https://rp.atb.no/scripts/TravelMagic/TravelMagicWE.dll/svar'
    r = requests.get(link, params=payload)

    now = datetime.now()

    if r.status_code is SUCCESSFUL_REQUEST_CODE:
        soup = soup(r.content, 'html.parser')
        arrival_times = soup.findAll('span', {'class':'tm-departurelist-time'})
        busses = soup.findAll('strong', {'class':'tm-departurelist-linename'})

        for bus, bustime in zip(busses[:rows], arrival_times[:rows]):
            arrival = bustime.text.replace('\n','').replace(' ','')
            remaining = remaining_minutes(arrival, now)
            if remaining <= 15:
                arrival = '{} min'.format(remaining)
            results.append({'bus': bus.text.rstrip(),
                            'arrival': arrival.replace('\r','')})

    else:
        raise UserWarning('Error making request, status code: {}'
                          .format(r.status_code))

    return results


if __name__ == "__main__":
    results = get_departues(3)
    for res in results:
        print(res)
