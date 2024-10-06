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

whole_list = list()
exceptions = ['asset', 'management', 'capital', 'managing', 'investment',
              'limited', 'plc', 'drc', 'nv']

for row in rows[1:]:
    cells = row.findChildren('td')
    exists = False
    try:
        titles = cells[2].text.replace(')', '').split('(')
        title_0 = titles[0].split()
        for item in exceptions:
            if item in [x.lower() for x in title_0]:
                exists = True
                break
        if len(title_0) > 1 and exists is False:
            company_list = [round(float(cells[5].text.replace('%', '').strip()),
                                  2),
                            round(float(cells[6].text.replace('%', '').strip()),
                                  2),
                            round(float(cells[7].text.replace('%', '').strip()),
                                  2)]
            whole_list.append((titles[-1], company_list))
    except:
        continue

sorted_whole_list_1 = sorted(whole_list, key=lambda x: x[1][0], reverse=True)
print(sorted_whole_list_1)
sorted_whole_list_2 = sorted(whole_list, key=lambda x: x[1][1], reverse=True)
sorted_whole_list_3 = sorted(whole_list, key=lambda x: x[1][2], reverse=True)

fhand = open('C:\django_projects\myproject\Result_parse_best_companies.txt',
             'w')
fhand.write('__Отсортированы по 3 м__' + '\n\n')
for el in sorted_whole_list_1:
    fhand.write('\n' + el[0] + ': ' + str(el[1][0]) + ' ' + str(el[1][1]) + ' '
                + str(el[1][2]) + '\n')
fhand.write('\n\n' + '__Отсортированы по 1 г__' + '\n\n')
for el in sorted_whole_list_2:
    fhand.write('\n' + el[0] + ': ' + str(el[1][0]) + ' ' + str(el[1][1]) + ' '
                + str(el[1][2]) + '\n')
fhand.write('\n\n' + '__Отсортированы по 5 г__' + '\n\n')
for el in sorted_whole_list_3:
    fhand.write('\n' + el[0] + ': ' + str(el[1][0]) + ' ' + str(el[1][1]) + ' '
                + str(el[1][2]) + '\n')
fhand.close()
