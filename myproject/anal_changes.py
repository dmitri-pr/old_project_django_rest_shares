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

sfrw_price_down = list()
lfrw_price_down = list()
sfrw_price_below_book = list()
lfrw_price_below_book = list()
sfrw_price_below_curr = list()
lfrw_price_below_curr = list()
sfrw_price_up = list()
lfrw_price_up = list()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

r = requests.get("http://localhost:8000/parsanalyze")
print(r.text)

if r.text:
    d = json.loads(r.text)
    print(d)

for item in d:
    url = (
            "https://walletinvestor.com/mcx-stock-forecast/"
            + str(item["title"]).lower()
            + "-stock-prediction"
    )
    document = urlopen(url, context=ctx)
    html = document.read()

    soup = BeautifulSoup(html, "html.parser")

    title_ = soup.find(
        lambda tag: tag.name == "h1"
                    and tag.find("a", attrs={"class": "prediction-title-link"})
    )
    title = title_.find("a").text
    print(title)

    curr_taglist = soup.find_all("a", class_="forecast-currency-href")
    for el in curr_taglist:
        if el.find("span", class_="number bignum"):
            curr_price = el.find("span", class_="number bignum").text[1:].split()[0]
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

    if float(sfrw_price) < float(item["sfrw_price"]):
        sfrw_price_down.append(
            str(
                (
                    item["title"],
                    round(
                        (
                                (float(sfrw_price) - float(item["sfrw_price"]))
                                * 100
                                / float(item["sfrw_price"])
                        ),
                        2,
                    ),
                )
            )
        )
    if float(sfrw_price) > float(item["sfrw_price"]):
        sfrw_price_up.append(
            str(
                (
                    item["title"],
                    round(
                        (
                                (float(sfrw_price) - float(item["sfrw_price"]))
                                * 100
                                / float(item["sfrw_price"])
                        ),
                        2,
                    ),
                )
            )
        )
    if float(sfrw_price) < float(item["book_price"]):
        sfrw_price_below_book.append(
            str(
                (
                    item["title"],
                    round(
                        (
                                (float(sfrw_price) - float(item["book_price"]))
                                * 100
                                / float(item["book_price"])
                        ),
                        2,
                    ),
                )
            )
        )
    if float(sfrw_price) < float(curr_price):
        sfrw_price_below_curr.append(
            str(
                (
                    item["title"],
                    round(
                        (
                                (float(sfrw_price) - float(curr_price))
                                * 100
                                / float(curr_price)
                        ),
                        2,
                    ),
                )
            )
        )

    lfrw_taglist = soup.find_all("span", class_="bignum")
    for el in lfrw_taglist:
        if el.find("a", class_="forecast-currency-href"):
            lfrw_price = el.find("a", class_="forecast-currency-href").text.split()[0]
            print(lfrw_price)
            break

    if float(lfrw_price) < float(item["lfrw_price"]):
        lfrw_price_down.append(
            str(
                (
                    item["title"],
                    round(
                        (
                                (float(lfrw_price) - float(item["lfrw_price"]))
                                * 100
                                / float(item["lfrw_price"])
                        ),
                        2,
                    ),
                )
            )
        )
    if float(lfrw_price) > float(item["lfrw_price"]):
        lfrw_price_up.append(
            str(
                (
                    item["title"],
                    round(
                        (
                                (float(lfrw_price) - float(item["lfrw_price"]))
                                * 100
                                / float(item["lfrw_price"])
                        ),
                        2,
                    ),
                )
            )
        )
    if float(lfrw_price) < float(item["book_price"]):
        lfrw_price_below_book.append(
            str(
                (
                    item["title"],
                    round(
                        (
                                (float(lfrw_price) - float(item["book_price"]))
                                * 100
                                / float(item["book_price"])
                        ),
                        2,
                    ),
                )
            )
        )
    if float(lfrw_price) < float(curr_price):
        lfrw_price_below_curr.append(
            str(
                (
                    item["title"],
                    round(
                        (
                                (float(lfrw_price) - float(curr_price))
                                * 100
                                / float(curr_price)
                        ),
                        2,
                    ),
                )
            )
        )

    upload = {
        "title": title,
        "curr_price": curr_price,
        "sfrw_price": sfrw_price,
        "lfrw_price": lfrw_price,
    }
    r = requests.put(
        "http://localhost:8000/parsanalyze/" + str(item["id"]) + "/", data=upload
    )

fhand = open("C:\django_projects\myproject\Result_anal_changes.txt", "w")
fhand.write("__Негатив__" + "\n\n")
fhand.write("Краткосрочный прогноз вниз:" + "\n" + " ".join(sfrw_price_down) + "\n")
fhand.write("Долгосрочный прогноз вниз:" + "\n" + " ".join(lfrw_price_down) + "\n")
fhand.write("\n\n" + "__Настораживающий негатив__" + "\n\n")
fhand.write(
    "Краткосрочный прогноз ниже текущей цены:"
    + "\n"
    + " ".join(sfrw_price_below_curr)
    + "\n"
)
fhand.write(
    "Долгосрочный прогноз ниже текущей цены:"
    + "\n"
    + " ".join(lfrw_price_below_curr)
    + "\n"
)
fhand.write("\n\n" + "__Сильный негатив__" + "\n\n")
fhand.write(
    "Краткосрочный прогноз ниже цены покупки:"
    + "\n"
    + " ".join(sfrw_price_below_book)
    + "\n"
)
fhand.write("\n\n" + "__Чрезвычайный негатив__" + "\n\n")
fhand.write(
    "Долгосрочный прогноз ниже цены покупки:"
    + "\n"
    + " ".join(lfrw_price_below_book)
    + "\n"
)
fhand.write("\n\n" + "__Позитив__" + "\n\n")
fhand.write("Краткосрочный прогноз вверх:" + "\n" + " ".join(sfrw_price_up) + "\n")
fhand.write("Долгосрочный прогноз вверх:" + "\n" + " ".join(lfrw_price_up) + "\n")
fhand.close()

now = datetime.datetime.now()

fhand = open("C:\django_projects\myproject\Result_anal_changes_log.txt", "a")
fhand.write("\n\n" + "|||||_____Дата и время: " + str(now) + "____|||||" + "\n\n")
fhand.write("__Негатив__" + "\n\n")
fhand.write("Краткосрочный прогноз вниз:" + "\n" + " ".join(sfrw_price_down) + "\n")
fhand.write("Долгосрочный прогноз вниз:" + "\n" + " ".join(lfrw_price_down) + "\n")
fhand.write("\n\n" + "__Настораживающий негатив__" + "\n\n")
fhand.write(
    "Краткосрочный прогноз ниже текущей цены:"
    + "\n"
    + " ".join(sfrw_price_below_curr)
    + "\n"
)
fhand.write(
    "Долгосрочный прогноз ниже текущей цены:"
    + "\n"
    + " ".join(lfrw_price_below_curr)
    + "\n"
)
fhand.write("\n\n" + "__Сильный негатив__" + "\n\n")
fhand.write(
    "Краткосрочный прогноз ниже цены покупки:"
    + "\n"
    + " ".join(sfrw_price_below_book)
    + "\n"
)
fhand.write("\n\n" + "__Чрезвычайный негатив__" + "\n\n")
fhand.write(
    "Долгосрочный прогноз ниже цены покупки:"
    + "\n"
    + " ".join(lfrw_price_below_book)
    + "\n"
)
fhand.write("\n\n" + "__Позитив__" + "\n\n")
fhand.write("Краткосрочный прогноз вверх:" + "\n" + " ".join(sfrw_price_up) + "\n")
fhand.write("Долгосрочный прогноз вверх:" + "\n" + " ".join(lfrw_price_up) + "\n")
fhand.close()
