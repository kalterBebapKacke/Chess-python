import noideacore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
from bs4 import BeautifulSoup
import os
import chess
import chess.engine
import multiprocessing as mp

training = "https://lichess.org/training"
inf = float('inf')
neg_inf = float('-inf')

def get_training_fen(arg):
    service = ChromeService()
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(training)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    try:
        time.sleep(5)
        source = driver.page_source
        button = driver.find_element(By.CLASS_NAME, 'view_solution')
        button.click()
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        fen = str(soup.find(title="Spiele mit dem Computer"))
        fen = fen[fen.find('href="/analysis/') + len('href="/analysis/'):]
        fen = fen[:fen.find('?')].replace('_', ' ')
        driver.quit()
        return fen
    except Exception:
        driver.quit()
        return False

def get_path():
    path = os.getcwd()
    path += r'\stockfish\stockfish-windows-x86-64-avx2.exe'
    return path

def get_eval(fens:list):
    engine = chess.engine.SimpleEngine.popen_uci(get_path())
    results = list()
    for fen in fens:
        board = chess.Board(fen)
        result = engine.analyse(board, chess.engine.Limit(time=0.5))['score']
        result = str(result.white())
        if str(result).__contains__('#'):
            pass
        else:
            result = float(result) / 100
            results.append([fen, result])
    engine.quit()
    return results

def sqlite3():
    sql = noideacore.sql.SQL_Class('sqlite')
    path = os.getcwd()
    path = path[:path.find(r'\get_data')]
    path += r'\database.db'
    sql.login(database=path, tables=['chess_data'])
    return sql

def main(length:int=20,process:int=4):
    pool = mp.Pool(process)
    arg = ['' for x in range(length)]
    res = pool.map(get_training_fen, arg)
    res = list(filter(lambda x: x != False, res))
    res = get_eval(res)
    sql = sqlite3()
    for x in res:
        sql.basic_write(None, fen=x[0], eval=x[1])







if __name__ == "__main__":
    t_fen = 'r2q1rk1/1p1bbppp/p2p4/3np1B1/2B1P3/8/PPP2PPP/R2QR1K1_w_-_-_0_13'.replace('_', ' ')
    fen2 = '8/8/8/8/8/1k6/7q/K7 b - - 0 1'
    fen3 = '8/8/8/8/8/1K6/7Q/k7 w - - 0 1'
    #print(get_eval([fen2]))
    main(2)


