from hktraffic import proxies
from hktraffic.models import Arrival, Departure, Traffic

from bs4 import BeautifulSoup
from django.db import IntegrityError
from django.utils import timezone

import os
import requests


BASE_URL = 'https://www.immd.gov.hk'
HOME_URL = '/eng/message_from_us/stat_menu.html'


def convert_csv(filepath=''):

    if not filepath:
        filepath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    headers = ['date', 'control_point', 'arrivals_residents', 'arrivals_chinavisitors', 'arrivals_othervisitors', 'arrivals_total', 'departures_residents', 'departures_chinavisitors', 'departures_othervisitors', 'departures_total', 'weekday']
    headers = ','.join(headers)
    traffic = Traffic.objects.all()
    with open(f'{filepath}/HKtraffic.csv', 'w') as f:
        f.write(headers)
        f.write('\n')
        for t in traffic:
            row = [t.date, t.control_point, t.arrivals.residents, t.arrivals.chinavisitors, t.arrivals.othervisitors, t.arrivals.total, t.departures.residents, t.departures.chinavisitors, t.departures.othervisitors, t.departures.total, t.weekday]
            row = [str(item) for item in row]
            row = ','.join(row)
            f.write(row)
            f.write('\n')
    return


def getlinks(link: str):

    # to get homepage, set input to HOME_URL. this will return list of all monthly links
    # monthly links can be used as the input here to obtain all daily links
    soup = getpage(link)
    links = [link.a['href'] for link in soup.ul if link != '\n']

    return links


def getpage(link: str):

    # input should be the extension provided from monthlytraffic() or get_monthlylinks()
    # returns the soup object of a page
    if link[0:4] == 'http':
        url = link
    else:
        url = f'{BASE_URL}{link}'
    proxy = proxies.getproxy()
    response = requests.get(url, proxies=proxy)
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup


def scrapeday(link: str):

    # input should be an output from the list of getlinks() pertaining to days in a month
    soup = getpage(link)

    _date = soup.find('td', attrs={'class': 'table-sub table-sub-center', 'id': 'sub-Date'}).text
    date = timezone.datetime.strptime(_date, '%d %B %Y').date()
    weekday = soup.tbody.tr.find('td', attrs={'id': 'sub-Week'}).text
    rows = soup.tbody.findAll('tr')
    for row in rows:
        control_point = row.find('td', attrs={'data-label': 'Control Point'}).text
        traffic_id = f'{control_point}_{str(date)}'
        arrivals_residents = int(row.find('td', attrs={'headers': 'Hong_Kong_Residents_Arrival'}).text.replace(',',''))
        arrivals_chinavisitors = int(row.find('td', attrs={'headers': 'Mainland_Visitors_Arrival'}).text.replace(',',''))
        arrivals_othervisitors = int(row.find('td', attrs={'headers': 'Other_Visitors_Arrival'}).text.replace(',',''))
        arrivals_total = int(row.find('td', attrs={'headers': 'Total_Arrival'}).text.replace(',',''))
        departures_residents = int(row.find('td', attrs={'headers': 'Hong_Kong_Residents_Departure'}).text.replace(',',''))
        departures_chinavisitors = int(row.find('td', attrs={'headers': 'Mainland_Visitors_Departure'}).text.replace(',',''))
        departures_othervisitors = int(row.find('td', attrs={'headers': 'Other_Visitors_Departure'}).text.replace(',',''))
        departures_total = int(row.find('td', attrs={'headers': 'Total_Departure'}).text.replace(',',''))

        traffic = Traffic(traffic_id=traffic_id, date=date, control_point=control_point, weekday=weekday)
        try:
            traffic.save()
        except IntegrityError:
            pass

        arrival = Arrival(traffic=traffic, residents=arrivals_residents, chinavisitors=arrivals_chinavisitors, othervisitors=arrivals_othervisitors, total=arrivals_total)
        try:
            arrival.save()
        except IntegrityError:
            pass

        departure = Departure(traffic=traffic, residents=departures_residents, chinavisitors=departures_chinavisitors, othervisitors=departures_othervisitors, total=departures_total)
        try:
            departure.save()
        except IntegrityError:
            pass

    print(f'{str(date)} scraped')
    return


def update(date=timezone.now().date()):

    # first iteration starts by evaluating yesterday. Each iteration works back a day until db records are found
    date -= timezone.timedelta(days=1)

    # pad a 0 for month and day if needed
    if len(str(date.month)) == 1:
        month = f'0{date.month}'
    else:
        month = date.month
    if len(str(date.day)) == 1:
        day = f'0{date.day}'
    else:
        day = date.day
    year = str(date.year)

    link = f'/eng/stat_{year}{month}{day}.html'
    if Traffic.objects.filter(date=date).count() == 0:
        try:
            scrapeday(link)
        except AttributeError:
            pass  # this means page does not exist. Usually only happens for the current day
        update(date)
    return
