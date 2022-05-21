import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import Gyeongnam.Masan
import Gyeongnam.Yangsan
import Gyeongnam.Jinju
import Gyeongnam.Changwon
import Busan.Busan
import Jeonbuk.Jeonbuk
import Jeonbuk.Jeonbuk_ency
import Jeonbuk.Jeonju
import Seoul.Eunpyeong
import w_Country.HereT
import w_Country.FleaMarket
import w_Country.Worknet
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'

    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=" + user_agent)

    # options.add_argument('headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--proxy-server=https://%s' % PROXY)

    announcement_list = []
    try:
        announcement_list_Worknet = w_Country.Worknet.main()
        # print(announcement_list_Worknet)
        announcement_list.extend(announcement_list_Worknet)

    except NoSuchElementException:
        pass

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        announcement_list_FleaMarket = w_Country.FleaMarket.main(driver)
        # print(announcement_list_Gyeongnam_Masan)
        announcement_list.extend(announcement_list_FleaMarket)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Gyeongnam_Masan = Gyeongnam.Masan.main(driver)
        # print(announcement_list_Gyeongnam_Masan)
        announcement_list.extend(announcement_list_Gyeongnam_Masan)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Gyeongnam_Yangsan = Gyeongnam.Yangsan.main(driver)
        # print(announcement_list_Gyeongnam_Yangsan)
        announcement_list.extend(announcement_list_Gyeongnam_Yangsan)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Gyeongnam_Jinju = Gyeongnam.Jinju.main(driver)
        # print(announcement_list_Gyeongnam_Jinju)
        announcement_list.extend(announcement_list_Gyeongnam_Jinju)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Gyeongnam_Changwon = Gyeongnam.Changwon.main(driver)
        # print(announcement_list_Gyeongnam_Changwon)
        announcement_list.extend(announcement_list_Gyeongnam_Changwon)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Busan_Busan = Busan.Busan.main(driver)
        # print(announcement_list_Busan_Busan)
        announcement_list.extend(announcement_list_Busan_Busan)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Jeonbuk_Jeonbuk = Jeonbuk.Jeonbuk.main(driver)
        # print(announcement_list_Jeonbuk_Jeonbuk)
        announcement_list.extend(announcement_list_Jeonbuk_Jeonbuk)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Jeonbuk_Jeonbuk_ency = Jeonbuk.Jeonbuk_ency.main(driver)
        # print(announcement_list_Jeonbuk_Jeonbuk_ency)
        announcement_list.extend(announcement_list_Jeonbuk_Jeonbuk_ency)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Jeonbuk_Jeonju = Jeonbuk.Jeonju.main(driver)
        # print(announcement_list_Jeonbuk_Jeonju)
        announcement_list.extend(announcement_list_Jeonbuk_Jeonju)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Seoul_Eunpyeong = Seoul.Eunpyeong.main(driver)
        # print(announcement_list_Seoul_Eunpyeong)
        announcement_list.extend(announcement_list_Seoul_Eunpyeong)

    except NoSuchElementException:
        pass

    try:
        announcement_list_Here = w_Country.HereT.main(driver)
        # print(announcement_list_Here)
        announcement_list.extend(announcement_list_Here)

    except NoSuchElementException:
        pass

    with open('C:/Users/Admin/Documents/GitHub/capstone-2022-39/wholeCountry/announcement_list.json', 'w', encoding='UTF-8-sig') as f:
        f.write(json.dumps(announcement_list, ensure_ascii=False, indent=4))
