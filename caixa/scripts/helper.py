#!/usr/bin/python
#
# General Class
# Class create a intance with commom data
#
import re
import unidecode


class Helper:

    def __init__(self, contest, page):
        self.contest        = contest
        self.page           = page
        self.pattern_digits = re.compile(r'\d+')

    def remove_digits(list):
        pattern = '[0-9]'
        list = [re.sub(pattern, '', i) for i in list]
        return list

    def get_general(self):
        nro, day, mount, year = self.pattern_digits.findall(self.page.find(
                                "div", class_ ="title-bar").find(
                                "span", class_="ng-binding").text.replace(
                                    "\t", "").replace(
                                    "\n", ""))
        return {
            "nro"  : nro,
            "data" : day + "/" + mount + "/" + year
        }

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


    def get_next_prize_megasena(self, result_contest, related_box):
        data = {
            "valor"      : "R$ " + result_contest.find("div", class_="next-prize").text.replace("\n", "").replace("\t", "").split("R$")[1].replace(" ", ""),
            "data"       : "/".join(self.pattern_digits.findall(result_contest.find("div", class_="next-prize").text.replace("\n", "").replace("\t", ""))[:3]),
            "arrecadado" : related_box.find_all("strong", class_="ng-binding")[-1].text,
            "estimado"   : result_contest.find("div", class_="next-prize").find("p", class_="value").text
        }
        data["outros"] = {}
        for hj in result_contest.find("div", class_="totals").find_all("p"):
            a = unidecode.unidecode(hj.find("span").text).lower().replace(
                "\t", "" ).replace(
                "\n", "" ).replace(
                " " , "_").replace(
                "(" , "" ).replace(
                ")" , "" )
            name = re.sub('[0-9]', '', a)
            data["outros"][name] = "R$ " + hj.find("span", class_="value").text.split("R$")[1].replace(" ", "")
        return data
