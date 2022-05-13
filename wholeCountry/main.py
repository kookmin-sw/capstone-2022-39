import json
from selenium import webdriver
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
import w_Country.Here
import w_Country.Worknet
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == '__main__':
    driver = webdriver.Chrome(ChromeDriverManager().install())
    announcement_list = []

    announcement_list_Gyeongnam_Masan = Gyeongnam.Masan.main(driver)
    # print(announcement_list_Gyeongnam_Masan)
    announcement_list.extend(announcement_list_Gyeongnam_Masan)

    announcement_list_Gyeongnam_Yangsan = Gyeongnam.Yangsan.main(driver)
    # print(announcement_list_Gyeongnam_Yangsan)
    announcement_list.extend(announcement_list_Gyeongnam_Yangsan)

    announcement_list_Gyeongnam_Jinju = Gyeongnam.Jinju.main(driver)
    # print(announcement_list_Gyeongnam_Jinju)
    announcement_list.extend(announcement_list_Gyeongnam_Jinju)

    announcement_list_Gyeongnam_Changwon = Gyeongnam.Changwon.main(driver)
    # print(announcement_list_Gyeongnam_Changwon)
    announcement_list.extend(announcement_list_Gyeongnam_Changwon)

    announcement_list_Busan_Busan = Busan.Busan.main(driver)
    # print(announcement_list_Busan_Busan)
    announcement_list.extend(announcement_list_Busan_Busan)

    announcement_list_Jeonbuk_Jeonbuk = Jeonbuk.Jeonbuk.main(driver)
    # print(announcement_list_Jeonbuk_Jeonbuk)
    announcement_list.extend(announcement_list_Jeonbuk_Jeonbuk)

    announcement_list_Jeonbuk_Jeonbuk_ency = Jeonbuk.Jeonbuk_ency.main(driver)
    # print(announcement_list_Jeonbuk_Jeonbuk_ency)
    announcement_list.extend(announcement_list_Jeonbuk_Jeonbuk_ency)

    announcement_list_Jeonbuk_Jeonju = Jeonbuk.Jeonju.main(driver)
    # print(announcement_list_Jeonbuk_Jeonju)
    announcement_list.extend(announcement_list_Jeonbuk_Jeonju)

    announcement_list_Seoul_Eunpyeong = Seoul.Eunpyeong.main(driver)
    # print(announcement_list_Seoul_Eunpyeong)
    announcement_list.extend(announcement_list_Seoul_Eunpyeong)

    # announcement_list_Here = w_Country.Here.main(driver)
    # print(announcement_list_Here)
    # announcement_list.extend(announcement_list_Here)

    announcement_list_Worknet = w_Country.Worknet.main()
    # print(announcement_list_Worknet)
    announcement_list.extend(announcement_list_Worknet)

    with open('C:/Users/Admin/Documents/GitHub/capstone-2022-39/wholeCountry/announcement_list.json', 'w', encoding='UTF-8-sig') as f:
        f.write(json.dumps(announcement_list, ensure_ascii=False, indent=4))
