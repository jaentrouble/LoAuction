from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import json
import time

def datestring_parser(datestring:str):
    """datestring_parser
    format : YYYY-MM-DD hh:mm:ss
    """
    
    d, t = datestring.split(' ')
    YY, MM, DD = d.split('-')
    hh, mm, ss = t.split(':')
    return (
        int(YY),
        int(MM),
        int(DD),
        int(hh),
        int(mm),
        int(ss),
    )

def is_past(past:tuple, present:tuple):
    """
    format : (YY, MM, DD, hh, mm, ss)
    """
    if past[0] < present[0]:
        return True
    elif past[0] == present[0]:
        if past[1] < present[1]:
            return True
        elif past[1] == present[1]:
            if past[2] < present[2]:
                return True
            elif past[2] == present[2]:
                if past[3] < present[3]:
                    return True
                elif past[3] == present[3]:
                    if past[4] < present[4]:
                        return True
                    elif past[4] == present[4]:
                        if past[5] < present[5]:
                            return True
    
    return False
    
def item_parser(driver:WebDriver, i:int):
    """
    'i' should start from 1
    returns datetime, soldprice, startprice, raw_info(json loaded dictionary)
    """
    datestring = driver.find_element(By.XPATH,f'//*[@id="auctionListTbody"]/tr[{i}]/td[6]/div').text
    date_time = datestring_parser(datestring)
    sold_price_str = driver.find_element(By.XPATH,f'//*[@id="auctionListTbody"]/tr[{i}]/td[5]/div/em').text
    sold_price = int(sold_price_str.replace(',',''))
    start_price_str = driver.find_element(By.XPATH,f'//*[@id="auctionListTbody"]/tr[{i}]/td[4]/div/em').text
    start_price = int(start_price_str.replace(',',''))
    str_info =driver.find_element(By.XPATH,f'//*[@id="auctionListTbody"]/tr[{i}]/td[1]/div[1]/span[1]').get_attribute('data-item')
    dict_info = json.loads(str_info)

    return date_time, sold_price, start_price, dict_info

def refresh_login(driver):
    """
    re-login and get back to auction-stats-accessory page
    """
    driver.get('https://member.onstove.com/auth/login')
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="user_id"]').send_keys('insidemyelevator@gmail.com')
    driver.find_element(By.XPATH, '//*[@id="user_pwd"]').send_keys('gay74@stove')
    driver.find_element(By.XPATH, '//*[@id="idLogin"]/div[4]/button').click()
    time.sleep(3)
    driver.get('https://lostark.game.onstove.com/Auction/Stats')
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[1]/ul/li[4]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[1]/ul/li[4]/ul/li[1]').click()