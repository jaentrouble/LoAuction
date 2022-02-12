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

def datum_parser(datum:list):
    timestamp, _, price, info = datum
    parsed = {}
    parsed['year'] = timestamp[0]
    parsed['month'] = timestamp[1]
    parsed['day'] = timestamp[2]
    parsed['hour'] = timestamp[3]
    parsed['min'] = timestamp[4]
    parsed['sec'] = timestamp[5]
    name = info['Element_000']['value'].split('<')[-3].split('>')[-1]
    grade = info['Element_001']['value']['slotData']['iconGrade']
    acc_type = info['Element_001']['value']['leftStr0'].split('<')[-3].split('>')[-1].split(' ')[1]
    tier = int(info['Element_001']['value']['leftStr2'].split('<')[-2][-1])
    quality = info['Element_001']['value']['qualityValue']
    trade = int(info['Element_003']['value'].split('<')[3][-1])

    parsed['price'] = price
    parsed['name'] = name
    parsed['grade'] = grade
    parsed['acc_type'] = acc_type
    parsed['tier'] = tier
    parsed['quality'] = quality
    parsed['trade'] = trade

    if acc_type == '목걸이':
        #특성
        e_1_name = info['Element_007']['value']['Element_001'].split('<BR>')[0].split(' +')[0]
        e_1_val = int(info['Element_007']['value']['Element_001'].split('<BR>')[0].split('+')[1])
        e_2_name = info['Element_007']['value']['Element_001'].split('<BR>')[1].split(' +')[0]
        e_2_val = int(info['Element_007']['value']['Element_001'].split('<BR>')[1].split('+')[1])
        parsed['e_1_name'] = e_1_name
        parsed['e_1_val'] = e_1_val
        parsed['e_2_name'] = e_2_name
        parsed['e_2_val'] = e_2_val
        #각인
        en_strs = info['Element_008']['value']['Element_001'].split('<BR>')
        for i, s in enumerate(en_strs):
            en_name = s.split('</FONT>')[0].split('>')[1]
            en_val = int(s.split('+')[-1])
            parsed[f'en_{i+1}_name'] = en_name
            parsed[f'en_{i+1}_val'] = en_val

    elif acc_type == '팔찌':
        op_str = info['Element_006']['value']['Element_001']
        unlocked = op_str.count('changeable')
        i = 0 #manual because of '속공' option
        for s in op_str.split('<BR>'):
            if s.count('changeable'):
                pass
            elif s.count('['):
                name = s.split('[')[1].split(']')[0].replace("<FONT COLOR='#f9f7d0'>",'').replace('</FONT>','')
                spec = s.split(']')[1]
                parsed[f'option_{i+1}_name'] = name
                parsed[f'option_{i+1}_spec'] = spec
                i += 1

            elif s.count('+'):
                name = s.split(' +')[0].split('</img> ')[1]
                spec = int(s.split('+')[1])
                parsed[f'option_{i+1}_name'] = name
                parsed[f'option_{i+1}_spec'] = spec
                i += 1
            elif s.count('속공'):
                pass
            else:
                raise Exception(f'unhandled wrist option:{s}')
        parsed['changeable_options'] = unlocked
    elif acc_type in ['귀걸이','반지']:
        # 특성
        e_name, e_val = info['Element_007']['value']['Element_001'].split(' +')
        e_val = int(e_val)
        parsed['e_name'] = e_name
        parsed['e_val'] = e_val
        #각인
        en_strs = info['Element_008']['value']['Element_001'].split('<BR>')
        for i, s in enumerate(en_strs):
            en_name = s.split('</FONT>')[0].split('>')[1]
            en_val = int(s.split('+')[-1])
            parsed[f'en_{i+1}_name'] = en_name
            parsed[f'en_{i+1}_val'] = en_val
    return parsed