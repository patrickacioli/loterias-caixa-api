#!/usr/bin/python
#
# Megasena Script
# Get data of megasena contest
#
import json
from caixa.scripts import helper as hp


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
            "proximo"   : self.helper.get_next_prize_megasena(self.result_contest, self.related_box),
            "premiacao" : self.helper.get_prizes(self.related_box)
        }



        return json.dumps(data)
