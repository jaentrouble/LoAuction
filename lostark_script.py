from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lostark.lostark_tools import *
from selenium.common.exceptions import NoSuchElementException
import json

MAX_PAGE = 5

driver = webdriver.Chrome('chromedriver')

input('finished?')

last_dt = (0,0,0,0,0,0)

logger_name = time.strftime('%Y_%m_%d_%H_%M.log')
refresh_time = time.time()

while True:
    logger = open(logger_name,'a')
    if time.time()-refresh_time > 3600:
        log_txt = '1 Hr passed... Refreshing...'
        print(log_txt)
        logger.write(log_txt+'\n')
        refresh_login(driver)
        refresh_time = time.time()
    logger.write(time.ctime()+'\n')
    logger.write('Search button click\n')
    print(time.ctime())
    print('Search button click')
    btn = driver.find_element(By.ID,'btnSearch')
    driver.execute_script('arguments[0].click();',btn)
    time.sleep(6)
    cur_log = []

    # Search at maximum 5 page per minute
    for page in range(MAX_PAGE):
        if page>0:
            print(f'page{page+1}')
            driver.find_element(By.XPATH,f'//*[@id="auctionList"]/div[2]/a[{page+2}]').click()
            time.sleep(6)

        # If banned, wait 10 minutes
        try:
            sample_ds = driver.find_element(By.XPATH,'//*[@id="auctionListTbody"]/tr[1]/td[6]/div').text
            if sample_ds == '':
                # if logged out, re-login
                refresh_login(driver)
            sample_dt = datestring_parser(sample_ds)
        except NoSuchElementException:
            logger.write(time.ctime()+'\n')
            logger.write('No element found, waiting 10 minutes\n')
            print(time.ctime())
            print('Waiting 10 minutes')
            time.sleep(600)
            break
        loop = True
        for i in range(1,11):
            datum = item_parser(driver, i)
            dt = datum[0]
            if is_past(last_dt, dt):
                cur_log.append(datum)
            else:
                loop = False
                break

        if loop==False:
            break
    
    if len(cur_log)>0:
        logger.write(time.ctime()+'\n')
        logger.write(f'total {len(cur_log)} items found\n')
        print(f'total {len(cur_log)} items found')
        name = str(sample_dt)+'.json'
        with open(f'accessory_logs/{name}','w') as f:
            json.dump(cur_log,f)
    last_dt = sample_dt
    logger.close()
    time.sleep(max(0,60-page*5))
