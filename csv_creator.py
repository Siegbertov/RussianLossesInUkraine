from bs4 import BeautifulSoup as bs
import requests
import csv
import re


def main():
    url = "https://index.minfin.com.ua/ua/russian-invading/casualties/"
    extra_url = "http://index.minfin.com.ua/ua/{}"

    last_months_ids = []
    data_list = []

    req = requests.get(url)
    req.encoding = 'utf-8'
    soup = bs(req.text, "html.parser")

    # Appending opened data
    for element in soup.find("ul", class_="see-also").find_all("li", class_="gold"):
        date = element.find("span", class_="black").text
        tank_quantity = re.findall(r"[0-9]+", element.find("div", class_="casualties").find_all("li")[0].text)
        ork_quantity = re.findall(r" (.*?) осіб", element.find("div", class_="casualties").find_all("li")[-1].text)[0].split()[-1]
        data_list.append(
            {
                "date": date,
                "tanks": int(tank_quantity[0]),
                "troops": int(ork_quantity)
            }
        )

    # Appending hidden data
    for el in soup.find_all("div", class_="ajaxmonth"):
        new_req = requests.get(extra_url.format(el.find("a")['href']))
        new_req.encoding = 'utf-8'
        new_soup = bs(new_req.text, "html.parser")
        list_of_days = new_soup.find_all("ul", class_="see-also")[1]
        for day in list_of_days:
            for x in day.find_all("span", class_="black"):
                date = x.text
                tank_quantity = x.parent.find("div", class_="casualties").find_all("li")[0].text
                tank_quantity = re.findall(r"[0-9]+", tank_quantity)
                ork_quantity = re.findall(r" (.*?) осіб", x.parent.find("div", class_="casualties").find_all("li")[-1].text)[
                    0].split()[-1]
                data_list.append(
                    {
                        "date": date,
                        "tanks": int(tank_quantity[0]),
                        "troops": int(ork_quantity)
                    }
                )

    # Creating CSV File
    with open("enemy_loses.csv", "w", encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Tanks", "Troops"])
        for day in data_list:
            current_row = []
            for k in day.keys():
                current_row.append(day[k])
            writer.writerow(current_row)


main()

