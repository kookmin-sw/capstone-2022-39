import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from wholeCountry.areas_of_recruitment import areas_of_recruitment
import json


def extract_url(soup):
    title_name_and_detail_link_list = list()

    announments = soup.select_one('ul#rsList02')
    titles = announments.select('li > div.info > a > div.info-tit > strong')
    links = announments.select('li > div.info > a')
    markUps = announments.select('li > div.info > a > div.info-proc > span.badge-info')

    for title, mark, link in zip(titles, markUps, links):
        if mark.get_text() == "접수중":
            title_name_and_detail_link_list.append([title.get_text(), link.attrs['href']])
        else:
            pass

    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, announments_list, announcement_list_Here, keyword):
    for announment in announments_list:
        # 추출된 URL(자바 스크립트 페이지)로 이동
        driver.execute_script(announment[1])
        time.sleep(1)

        # 다시 page_source 추출
        # soup = BeautifulSoup(driver.page_source, "html.parser")

        # 근무지 추출
        workplace = driver.find_element(By.XPATH, '//*[@id="dDtlWorkArea"]').text
        if workplace == "":
            workplace = keyword

        # 모집 인원 추출
        recruitment_staff = driver.find_element(By.XPATH,
                                                '//*[@id="dWokerCnt"]').text

        # 우대 사항 추출
        qualification_license = '-'

        # 내용 추출
        job_specifications = driver.find_element(By.XPATH,
                                                 '//*[@id="dDetCnts"]').text

        # 고용 형태 추출
        employment = driver.find_element(By.XPATH,
                                         '//*[@id="dProjType"]/div/strong').text

        # 급여액 추출
        wages = driver.find_element(By.XPATH,
                                    '//*[@id="detailDiv"]/div[2]/ul/li[3]/div/div/div[2]/dl[4]/dd').text

        # 근무 시간 추출
        business_hours = driver.find_element(By.XPATH,
                                             '//*[@id="detailDiv"]/div[2]/ul/li[3]/div/div/div[2]/dl[2]/dd').text

        # 채용 담당자 추출
        recruiter = driver.find_element(By.XPATH, '//*[@id="dCoNm_2"]').text

        # 연락처 추출
        contact_address = driver.find_element(By.XPATH, '//*[@id="dTelNo"]').text

        # 모집 분야
        recruitment_field = areas_of_recruitment(announment[0] + job_specifications)

        data = {
            'title': announment[0],
            'url': announment[1],
            'workplace': workplace,
            'recruitment_staff': recruitment_staff,
            'recruitment_field': recruitment_field,
            'qualification_license': qualification_license,
            'job_specifications': job_specifications,
            'employment': employment,
            'wages': wages,
            'business_hours': business_hours,
            'recruiter': recruiter,
            'contact_address': contact_address
        }

        announcement_list_Here.append(data)

    return announcement_list_Here


def pass_the_next_link(soup):
    announments = soup.select_one('div#paging02')
    next_link = announments.select('a')
    links = list()
    for link in next_link:
        links.append(link.attrs['href'])

    return links


def main(driver):
    url = 'https://www.seniorro.or.kr:4431/seniorro/main/main.do'
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 5초까지 기다려 준다.
    # driver.implicitly_wait(5)
    time.sleep(3)

    # 지속적으로 홈페이지에 오류가 나서 새로고침을 하도록 함.
    driver.refresh()
    time.sleep(3)

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Here = []

    # 일자리여기 검색창 Xpath
    xpath_text = '//*[@id="seachKeyword"]'
    # 검색하기 버튼
    xpath_button = '//*[@id="container_wr"]/div[1]/div[3]/button/i'

    # 지리 리스트
    f = open(r"C:\Users\Admin\Documents\GitHub\capstone-2022-39\wholeCountry\w_Country\district.txt", 'r',
             encoding="cp949")

    while True:
        keyword = f.readline()
        time.sleep(1)

        # 검색 창에 keyword 입력
        driver.find_element(By.XPATH, xpath_text).send_keys(keyword)
        time.sleep(1)
        # 검색 버튼 클릭하기
        try:
            driver.find_element(By.XPATH, xpath_button).click()
            time.sleep(1)
        except ElementClickInterceptedException:
            pass

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 페이지 URL들을 가지고 온다.
        next_link = pass_the_next_link(soup)
        detail_link_list = list()

        # 필요한 URL만 리스트에 추가함.
        for i in range(2, len(next_link) - 1):
            # print(next_link[i])
            detail_link_list.append(next_link[i])

        # 페이지 개수만큼 반복문 돌리기
        for detail_link in detail_link_list:
            try:
                # 공고 이름과 자세히 볼 수 있는 URL 얻음
                announments_list = extract_url(soup)
                # print(announments_list)

                time.sleep(2)
                # 자세한 공고로 접속하여 관련 data 수집
                announcement_list_Here = approach_detail_link_and_extract_recruitment_info(driver, announments_list,
                                                                                           announcement_list_Here, keyword)

                time.sleep(2)
                # 다음 페이지로 이동
                driver.execute_script(detail_link)

                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
            except NoSuchElementException:
                pass
        if not keyword:
            break
        driver.get(url)
    f.close()

    driver.close()
    driver.quit()

    return announcement_list_Here
