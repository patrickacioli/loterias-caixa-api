#!/usr/bin/python
#
# Megasena Script
# Get data of megasena contest
#
import json
import caixa.scripts.helper as hp
import re 
import unidecode


class Megasena:

    def __init__(self, driver):

        # Loading contest page
        self.page = driver.get(
            "http://localhost/pages/megasena.html",
            element_wait="title-bar",
            element_type="class"
        )
        self.helper = hp.Helper("megasena", self.page)
        self.result_contest = self.page.find("div", class_="resultado-loteria")
        self.related_box    = self.page.find("div", class_="related-box")
        self.pattern_digits = re.compile(r'\d+')

    def get_prizes(self, related_box):
        contest_related_data = []
        for h in related_box.find_all("p", class_="description")[:3]:
            contest_dict = {}
            contest_related = (h.find("strong").text.split("-")[0].replace(" ", "").lower())
            n = h.text.replace("\n", "").replace("\t", "").split("R$")
            contest_dict[contest_related] = {}
            if len(n) != 1:
                contest_dict[contest_related]["numero_ganhadores"] = int(self.pattern_digits.findall(n[0])[1])
                contest_dict[contest_related]["valor"] = n[1].replace(" ", "R$ ")
            else:
                contest_dict[contest_related]["numero_ganhadores"] = 0
                contest_dict[contest_related]["valor"] = 0
            contest_related_data.append(contest_dict)
        return contest_related_data


    def get_next_prize(self, result_contest, related_box):
        data = {
            "valor"      : "R$ " + result_contest.find("div", class_="next-prize").text.replace("\n", "").replace("\t", "").split("R$")[1].replace(" ", ""),
            "data"       : "/".join(self.pattern_digits.findall(result_contest.find("div", class_="next-prize").text.replace("\n", "").replace("\t", ""))[:3]),
            "arrecadado" : related_box.find_all("strong", class_="ng-binding")[-1].text,
            "estimado"   : result_contest.find("div", class_="next-prize").find_all("p", class_="value")[-1].text.replace("\t", "").replace("\n", "")
        }
        data["totais"] = {}
        for hj in result_contest.find("div", class_="totals").find_all("p"):
            a = unidecode.unidecode(hj.find("span").text).lower().replace(
                "\t", "" ).replace(
                "\n", "" ).replace(
                " " , "_").replace(
                "(" , "" ).replace(
                ")" , "" )
            name = re.sub('[0-9]', '', a)
            data["totais"][name] = "R$ " + hj.find("span", class_="value").text.split("R$")[1].replace(" ", "")
        return data

    def get_accumulated(self):
        return "ng-hide" not in self.result_contest.find("h3").attrs["class"]

    def get_numbers(self):
        return [n.text for n in self.result_contest.find("ul", class_="numbers").find_all("li")]

    def get_data(self):

        self.general = self.helper.get_general()
        data = {
            "numero"    : self.general["nro"],
            "data"      : self.general["data"],
            "acumulado" : self.get_accumulated(),
            "numeros"   : self.get_numbers(),
            "proximo"   : self.get_next_prize(self.result_contest, self.related_box),
            "premiacao" : self.get_prizes(self.related_box)
        }
        # temp 
        print(data)
        return json.dumps(data)
