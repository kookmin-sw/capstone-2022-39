"""
- selenium Ver : 3.14.1
- 마산노인일자리창출지원센터
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import os
from wholeCountry.areas_of_recruitment import areas_of_recruitment
import re
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    time.sleep(2)
    notices = driver.find_element(By.CLASS_NAME, 'scontent') \
        .find_element(By.CLASS_NAME, 'jobList') \
        .find_elements(By.TAG_NAME, 'dl')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices):
    title_name_and_detail_link_list = list()  # 제목 및 상세 페이지를 위한 URL 수집

    for notice in notices:
        try:
            section = notice.find_element(By.CLASS_NAME, 'msging').text
            if section == "모집중":
                detail_title = notice.find_element(By.CLASS_NAME, 'txt11b.nblue').text
                detail_link = notice.find_element(By.CLASS_NAME, 'txt11b.nblue') \
                    .get_attribute('href')

                registration_date = notice.find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')[3].text
                registration_date = registration_date.replace('.', '/')

                title_name_and_detail_link_list.append([detail_title, detail_link, registration_date[9:18]])
        except NoSuchElementException:
            pass

    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Gyeongnam_Masan):
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.get(str(detail_link_connect[1]))

        time.sleep(1)

        # 근무지 추출
        workplace = driver.find_element(By.XPATH, '//*[@id="scontainer"]/div/div/div[2]/div/div/table[1]/tbody/tr['
                                                  '1]/td[2]').text

        # 모집 인원 추출
        recruitment_staff = driver.find_element(By.XPATH,
                                                '//*[@id="scontainer"]/div/div/div[2]/div/div/table[1]/tbody/tr['
                                                '1]/td[4]').text

        # 모집 분야 추출
        recruitment_field = areas_of_recruitment(detail_link_connect[0])

        # 우대 사항 추출
        qualification_license = driver.find_element(By.XPATH,
                                                    '//*[@id="scontainer"]/div/div/div[2]/div/div/table[1]/tbody/tr['
                                                    '2]/td[4]').text
        # 내용 추출
        job_specifications = driver.find_element(By.XPATH,
                                                 '//*[@id="scontainer"]/div/div/div[2]/div/div/table[1]/tbody/tr['
                                                 '4]/td[2]').text

        # 고용 형태 추출
        employment = '-'

        # 급여액 추출
        wages = driver.find_element(By.XPATH,
                                    '//*[@id="scontainer"]/div/div/div[2]/div/div/table[1]/tbody/tr[2]/td[2]').text

        # 근무 시간 추출
        business_hours = driver.find_element(By.XPATH,
                                             '//*[@id="scontainer"]/div/div/div[2]/div/div/table[1]/'
                                             'tbody/tr[3]/td[2]').text

        # 채용 담당자 추출
        recruiter = "마산노인일자리창출지원센터 "

        # 연락처 추출
        contact_address = "055)246-6588"

        # 등록일
        registration_date = detail_link_connect[2]

        # primary key
        modify_title = re.sub('[^A-Za-z0-9가-힣]', '', detail_link_connect[0])
        modify_recruiter = re.sub('[^A-Za-z0-9가-힣]', '', recruiter)
        modify_workplace = re.sub('[^A-Za-z0-9가-힣]', '', workplace)
        primary_key = "M" + str(modify_title) + "#" + str(modify_recruiter) + "#" + str(modify_workplace)

        data = {
            'title': detail_link_connect[0],
            'url': detail_link_connect[1],
            'workplace': workplace,
            'recruitment_staff': recruitment_staff,
            'recruitment_field': recruitment_field,
            'qualification_license': qualification_license,
            'job_specifications': job_specifications,
            'employment': employment,
            'wages': wages,
            'business_hours': business_hours,
            'recruiter': recruiter,
            'contact_address': contact_address,
            'registration_date': registration_date,
            'primary_key': primary_key
        }

        announcement_list_Gyeongnam_Masan.append(data)

    return announcement_list_Gyeongnam_Masan


def pass_the_next_link(driver):
    links = driver.find_element(By.ID, 'pageDiv').find_elements(By.CLASS_NAME, 'page_links')

    return links


def main(driver):
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'http://www.masansj.com/sub/jobpy/?cGNvZGU9Mg=='

    # 웹드라이버 열기
    # options=options 추가해주기
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 5초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(5)

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Gyeongnam_Masan = []

    next_link = pass_the_next_link(driver)
    detail_link = list()
    for i in range(len(next_link)):
        detail_link.append(next_link[i].get_attribute('href'))

    index = 0
    while index < len(next_link):
        notices = approach_the_list(driver)
        detail_link_list = extract_url(notices)
        announcement_list_Gyeongnam_Masan = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Gyeongnam_Masan)

        driver.get(detail_link[index])

        index = index + 1
        time.sleep(1)

    return announcement_list_Gyeongnam_Masan
