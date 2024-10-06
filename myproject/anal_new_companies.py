import requests
import json
import urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://walletinvestor.com/best-russian-stocks-to-buy-mcx'
document = urlopen(url, context=ctx)
html = document.read()

soup = BeautifulSoup(html, "html.parser")
tables = soup.findChildren('table')
my_table = tables[0]
rows = my_table.findChildren('tr')

r = requests.get('http://localhost:8000/bestforbuying')
print(r.text)

d = json.loads(r.text)

l_entire = list()
l_added = list()
l_deleted = list()

for row in rows[1:]:
    cells = row.findChildren('td')
    try:
        titles = cells[2].text.replace(')', '').split('(')
        if titles[1] not in [x['short_title'] for x in d]:
            r = requests.post('http://localhost:8000/bestforbuying/',
                              data={'full_title': titles[0], 'short_title': titles[1]})
            l_added.append(titles[1])
        l_entire.append(titles[1])
    except:
        continue

for el in d:
    if el['short_title'] not in l_entire:
        r = requests.delete('http://localhost:8000/bestforbuying/' + str(
            el['id']))
        l_deleted.append(el['short_title'])

now = datetime.datetime.now()
fhand = open('C:\django_projects\myproject\Result_anal_new_companies_log.txt',
             'a')
fhand.write('\n\n' + '|||||_____Дата и время: ' + str(now) + '____|||||' + '\n\n')
fhand.write('__Добавлены__' + '\n\n')
fhand.write('\n' + ', '.join(l_added) + '\n')
fhand.write('\n\n' + '__Удалены__' + '\n\n')
fhand.write('\n' + ', '.join(l_deleted) + '\n')
fhand.close()
