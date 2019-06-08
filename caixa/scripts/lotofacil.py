#!/usr/bin/python
#
# Megasena Script
# Get data of megasena contest
#
import json
import caixa.scripts.helper as hp
import re 
import unidecode


class Lotofacil:

    def __init__(self, driver):

        # Loading contest page
        self.page = driver.get(
            "http://localhost/pages/lotofacil.html",
            element_wait="title-bar",
            element_type="class"
        )
        self.helper = hp.Helper("lotofacil", self.page)
        self.result_contest = self.page.find("div", class_="resultado-loteria")
        self.related_box    = self.page.find("div", class_="related-box")
        self.pattern_digits = re.compile(r'\d+')

    def get_accumulated(self):
        return "ng-hide" not in self.result_contest.find("h3").attrs["class"]

    def get_numbers(self):
        return [n.text for n in self.result_contest.find("table", class_="lotofacil").find_all("td")]


    def get_next_prize(self, result_contest, related_box):
        data = {
            "valor"      : "R$ " + self.result_contest.find("div", class_="next-prize").text.replace("\n", "").replace("\t", "").split("R$")[1].replace(" ", ""),
            "data"       : "/".join(self.pattern_digits.findall(self.result_contest.find("div", class_="next-prize").text.replace("\n", "").replace("\t", ""))[:3]),
            "arrecadado" : self.related_box.find_all("strong", class_="ng-binding")[-1].text,
            "estimado"   : self.result_contest.find("div", class_="next-prize").find_all("p", class_="value")[-1].text.replace("\t", "").replace("\n", "")
        }
        data["totais"] = {}
        for hj in result_contest.find_all("div", class_="totals"):
            a = unidecode.unidecode(hj.find("span").text).lower().replace(
                "\t", "" ).replace(
                "\n", "" ).replace(
                " " , "_").replace(
                "(" , "" ).replace(
                ")" , "" )
            name = re.sub('[0-9]', '', a)
            data["totais"][name] = "R$ " + hj.find("span", class_="value ng-binding").text.replace("\t", "").replace("\n", "").split("R$")[1]
        return data

    def get_data(self):

        self.general = self.helper.get_general()
        data = {
            "numero"    : self.general["nro"],
            "data"      : self.general["data"],
            "acumulado" : self.get_accumulated(),
            "numeros"   : self.get_numbers(),
            "proximo"   : self.get_next_prize(self.result_contest, self.related_box),
            # "premiacao" : #self.helper.get_prizes(self.related_box)
        }

        print(data)
        return json.dumps(data)
