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

url = "https://walletinvestor.com/best-russian-stocks-to-buy-mcx"
document = urlopen(url, context=ctx)
html = document.read()

soup = BeautifulSoup(html, "html.parser")
tables = soup.findChildren("table")
my_table = tables[0]
rows = my_table.findChildren("tr")

whole_list = list()
exceptions = [
    "asset",
    "management",
    "capital",
    "managing",
    "investment",
    "limited",
    "plc",
    "drc",
    "nv",
]

for row in rows[1:]:
    cells = row.findChildren("td")
    exists = False
    try:
        titles = cells[2].text.replace(")", "").split("(")
        title_0 = titles[0].split()
        print(titles[1])
        for item in exceptions:
            if item in [x.lower() for x in title_0]:
                exists = True
                break
        if len(title_0) > 1 and exists is False:
            url = (
                    "https://walletinvestor.com/mcx-stock-forecast/"
                    + titles[1].lower()
                    + "-stock-prediction"
            )
            document = urlopen(url, context=ctx)
            html = document.read()

            soup = BeautifulSoup(html, "html.parser")

            curr_taglist = soup.find_all("a", class_="forecast-currency-href")
            for el in curr_taglist:
                if el.find("span", class_="number bignum"):
                    curr_price = (
                        el.find("span", class_="number bignum").text[1:].split()[0]
                    )
                    print(curr_price)

            try:
                sfrw_price_ = soup.find_all(
                    lambda tag: tag.name == "td" and re.search("Price:", tag.text)
                )
                sfrw_price = sfrw_price_[len(sfrw_price_) - 1].text.split()[1].strip()
                print(sfrw_price)
            except:
                sfrw_price_ = soup.find("div", class_="forecast-price-target")
                sfrw_price_borders = sfrw_price_.find_all("strong")
                sfrw_price = round(
                    (
                            (
                                    float(sfrw_price_borders[0].text.strip())
                                    + float(sfrw_price_borders[1].text.strip())
                            )
                            / 2
                    ),
                    3,
                )
                print(sfrw_price)

            company_list = [
                round(
                    ((float(sfrw_price) - float(curr_price)) * 100 / float(curr_price)),
                    2,
                ),
                round(float(cells[5].text.replace("%", "").strip()), 2),
                round(float(cells[6].text.replace("%", "").strip()), 2),
                round(float(cells[7].text.replace("%", "").strip()), 2),
            ]
            whole_list.append((titles[-1], company_list))
    except:
        continue

sorted_whole_list_1 = sorted(whole_list, key=lambda x: x[1][0], reverse=True)
print(sorted_whole_list_1)
sorted_whole_list_2 = sorted(whole_list, key=lambda x: x[1][1], reverse=True)
sorted_whole_list_3 = sorted(whole_list, key=lambda x: x[1][2], reverse=True)
sorted_whole_list_4 = sorted(whole_list, key=lambda x: x[1][3], reverse=True)

fhand = open("C:\django_projects\myproject\Result_parse_best_companies.txt", "w")
fhand.write("__Отсортированы по 2 н__" + "\n\n")
for el in sorted_whole_list_1:
    fhand.write(
        "\n"
        + el[0]
        + ": "
        + str(el[1][0])
        + " "
        + str(el[1][1])
        + " "
        + str(el[1][2])
        + " "
        + str(el[1][3])
        + "\n"
    )
fhand.write("\n\n" + "__Отсортированы по 3 м__" + "\n\n")
for el in sorted_whole_list_2:
    fhand.write(
        "\n"
        + el[0]
        + ": "
        + str(el[1][0])
        + " "
        + str(el[1][1])
        + " "
        + str(el[1][2])
        + " "
        + str(el[1][3])
        + "\n"
    )
fhand.write("\n\n" + "__Отсортированы по 1 г__" + "\n\n")
for el in sorted_whole_list_3:
    fhand.write(
        "\n"
        + el[0]
        + ": "
        + str(el[1][0])
        + " "
        + str(el[1][1])
        + " "
        + str(el[1][2])
        + " "
        + str(el[1][3])
        + "\n"
    )
fhand.write("\n\n" + "__Отсортированы по 5 г__" + "\n\n")
for el in sorted_whole_list_4:
    fhand.write(
        "\n"
        + el[0]
        + ": "
        + str(el[1][0])
        + " "
        + str(el[1][1])
        + " "
        + str(el[1][2])
        + " "
        + str(el[1][3])
        + "\n"
    )

fhand.close()
