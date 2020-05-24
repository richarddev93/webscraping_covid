# -*- coding: utf-8 -*-
import time
import requests
import pandas as pd
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options  import Options
import json


cases ={}

def build_dict(type):
    
    print(" 1 - Iniciando busca dos dados do " + type + "...")
    url = "https://ncov2019.live/data/" + type
    #print("url:",url)
    
    option = Options()
    option.headless = True
    driver = webdriver.Firefox()

    driver.get(url)
    driver.implicitly_wait(10) 
    print(" 2 - Abrindo o navegador ..",url)
 
    
    
    element = driver.find_element_by_xpath("//*[@id='sortable_table_world']")
    html_content = element.get_attribute('outerHTML')
    
    soup = BeautifulSoup(html_content,'html.parser')
    table = soup.find(name='table')
    
    driver.quit() 
    print(" 3 - Fechando o navegador ...")

    print(" 4 - Estruturando dados ... ")
    df_full = pd.read_html(str(table))[0]
    df = df_full[['Name','Confirmed','Critical','Recovered','Active','Deceased']]
    df.columns = ['pais','confirmados','criticos','recuperados','ativos','mortos']
    
    cases[type] = df.to_dict('records')
    
    #Limpando os nomes dos paises  
    for j in cases['world']:
        j['pais'] = (j['pais'].replace('★  ',''))
        
    return cases


    
#Criando Json

js = json.dumps(build_dict('world'),indent=4)
print(' 5 - Gerando json ...')
fp = open('covid.json','w',encoding='utf-8')
fp.write(js)
fp.close()

print(' 6 - Arquivo Gerado ! ')



