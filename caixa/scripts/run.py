from caixa.scripts import webdriver as wb
from caixa.scripts import megasena

def run(contest):
    driver = wb.Webdriver(prefs=True, headless=True)
    try:
        if contest == "megasena":
            data = megasena.Megasena(driver).get_data()
    except Exception as a:
        return False
    finally:
        with open("static/json/%s.json" % contest, "w") as f_:
            f_.write(data)
            f_.close()
        return "Operação realizada com sucesso, novos dados disponíveis!!"
