from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import sys
import time as tm
import lxml
import requests as req
import re

price=[]
name=[]
specification={}
flag=0

def make_dataFrame():#make dataFrame
     global name
     global price
     global specification
     for i in range(0,len(name)):
          if 'name' in specification:
               specification['name'].append(name[i])
          else:
               specification['name']=[name[i]]
          if 'price' in specification:
               specification['price'].append(price[i]) 
          else:
               specification['price']=[price[i]]
     df=pd.DataFrame(specification)
     df.to_csv('C:\\Users\\Abhi\\Desktop\\data.csv')
     print(df)



def spec_data(keys_bs,data_bs,n):#specification data
     keys=[]
     data=[]
     reg_key=r'\<.*\"\>|\<.*\>'
     for i in range(0,len(keys_bs)):
          keys.append(re.sub(reg_key,"",str(keys_bs[i])))
          data.append(re.sub(reg_key,"",str(data_bs[i])))

     print(len(keys))
     diff_len=len(specification)-len(keys)
     if n==0:
          for i in range(0,len(keys)):
               specification[keys[i]]=[data[i]]
     else:
          for i in specification.keys():
               specification[i].append('NaN')
          for i in range(0,len(keys)):
               if keys[i] in specification:
                    specification[keys[i]][n]=data[i]
               else:
                    specification[keys[i]]=['NaN' for i in range(0,n)]
                    specification[keys[i]].append(data[i])  
     print(len(specification))



def name_price(nm,pr):# name and price 
     reg_nm=r"\[\<.*\"\>|\<.*\>\]"
     nm=re.sub(reg_nm,"",nm)
     name.append(nm)

     reg_pr=r"\[\<.*\"\>\W|\<.*\>\]"
     pr=re.sub(reg_pr,"",pr)
     price.append(pr)


def fetch_data(source,n):#fetch data
     
     soup2=BeautifulSoup(source,'lxml')

     
     filtr_price={'class','_1vC4OE _3qQ9m1'}
     price_bs=soup2.find_all('div',filtr_price)
     
     filtr_name={'class':'_35KyD6'}
     name_bs=soup2.find_all('span',filtr_name)
     
     name_price(str(name_bs),str(price_bs))       #for name and price

     filtr_keys={'class':'_3-wDH3 col col-3-12'}
     keys_bs=soup2.find_all('td',filtr_keys)

     filtr_data={'class':'_3YhLQA'}
     data_bs=soup2.find_all('li',filtr_data)

     spec_data(keys_bs,data_bs,n)         #for specification data
     
     




def fetch_links(driver):# getting all links
     soup=BeautifulSoup(driver.page_source,'lxml')
     filtr_links={'class':'_31qSD5'}
     links=soup.find_all('a',filtr_links)
     total_links=len(links)
     driver.execute_script("window.open('')")
     for i in range(0,5):
          print('iter : ',i)
          tm.sleep(4)
          driver.switch_to.window(driver.window_handles[1])
          link='https://flipkart.com'+links[i]['href']
          print(link)
          r=driver.get(link)
          fetch_data(driver.page_source,i)
          tm.sleep(6)
          driver.switch_to.window(driver.window_handles[0])
          
     driver.quit()
     make_dataFrame()
     
     

def search_bar(driver):# search bar and input
     bar=driver.find_element_by_name('q')
     bar.clear()
     bar.send_keys('gaming laptops')
     bar.send_keys(Keys.RETURN)
     r=driver.get(driver.current_url)
     fetch_links(driver)


def open_browser():#Automation start
     driver=webdriver.Chrome('C:\\webDriver\\chromedriver.exe')
     r=driver.get('https://flipkart.com')
     tm.sleep(2)
     if driver.find_element_by_css_selector('body > div.mCRfo9 > div > div > button'):
          btnx=driver.find_element_by_css_selector('body > div.mCRfo9 > div > div > button')
          btnx.click()
          
     search_bar(driver)
     
     
