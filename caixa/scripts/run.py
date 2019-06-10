from caixa.scripts import webdriver as wb
from caixa.scripts import megasena, lotofacil, quina

def run(contest):
    driver = wb.Webdriver(prefs=True, headless=True, client="firefox", executable=r'/usr/bin/geckodriver')
    try:
        if contest == "megasena":
            data = megasena.Megasena(driver).get_data()
        if contest == "lotofacil":
            data = lotofacil.Lotofacil(driver).get_data()
        if contest == "quina":
            data = quina.Quina(driver).get_data()
    except Exception as a:
        return a
    finally:
        with open("static/json/%s.json" % contest, "w") as f_:
            f_.write(data)
            f_.close()
        return "Operação realizada com sucesso, novos dados disponíveis!!"
