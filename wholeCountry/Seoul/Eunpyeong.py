"""
- selenium Ver : 3.14.1
- 은평어르신지원센터
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from wholeCountry.areas_of_recruitment import areas_of_recruitment
import re


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    time.sleep(3)
    notices = driver.find_element(By.CLASS_NAME, 'mdBoardTable') \
        .find_element(By.TAG_NAME, 'tbody').\
        find_elements(By.CLASS_NAME, 'md_mVer_Row')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices):
    title_name_and_detail_link_list = list()    # 제목 및 상세 페이지를 위한 URL 수집
    index = 0
    for notice in notices:
        if index < 15:
            index = index + 1
            pass
        else:
            detail_title = notice.find_element(By.CLASS_NAME, 'md_mVer_sbj').text
            detail_link = notice.find_element(By.CLASS_NAME, 'md_mVer_sbj').find_element(By.TAG_NAME, 'a')\
                .get_attribute('href')
            registration_date = notice.find_element(By.CLASS_NAME, 'md_mVer_info.mdTextOverflow').text

            if detail_title.__contains__("#"):
                title_name_and_detail_link_list.append([detail_title[5:], detail_link, registration_date[8:16]])
            else:
                title_name_and_detail_link_list.append([detail_title, detail_link, registration_date[8:16]])

    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Seoul_Eunpyeong):
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.get(str(detail_link_connect[1]))

        time.sleep(1)
        section_check = driver.find_element(By.XPATH, '//*[@id="AB_viewPrintArea"]/ul/li[1]/div/ul/span').text
        # print(section_check)

        if section_check == "[구인중]":
            # 근무지 추출
            try:
                workplace = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[1]/tbody/tr[2]/td['
                                                          '5]/span/strong/span').text

                # 모집인원 추출
                recruitment_staff = driver.find_element(By.XPATH,
                                                        '//*[@id="lightgallery"]/table[1]/tbody/tr[2]/td['
                                                        '4]/span/strong/span').text

                # 모집 분야 추출
                recruitment_field = areas_of_recruitment(detail_link_connect[0])

                # 우대 사항 추출
                if str(detail_link_connect[0]).__contains__("경비원"):
                    qualification_license = "경비경력자, 소방안전관리자 2급이상"
                else:
                    qualification_license = "-"

                # 내용 추출
                job_specifications = '-'

                # 고용 형태 추출
                try:
                    employment = driver.find_element(By.XPATH,
                                                     '//*[@id="lightgallery"]/table[1]/tbody/tr[2]/td[3]/span/strong/span').text
                except NoSuchElementException:
                    employment = "계약직"

                # 급여액 추출
                try:
                    wages = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[2]/tbody/tr[2]/td[1]/span/strong/span').text
                except NoSuchElementException:
                    wages = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[3]/tbody/tr[2]/td[1]/strong/span').text

                # 근무 시간 추출
                try:
                    business_hours = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[2]/tbody/tr[2]/td[2]/div/span/strong/span/span').text
                except NoSuchElementException:
                    business_hours = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[3]/tbody/tr[2]/td[2]/div/span/strong/span/span').text

                try:
                    business_form = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[2]/tbody/tr[2]/td[3]/span/strong/span').text
                except NoSuchElementException:
                    business_form = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[2]/tbody/tr[2]/td[3]/span').text

                # 채용 담당자 추출
                recruiter = "은평어르신일자리센터"

                # 연락처 추출
                contact_address = "070-7728-2807"

                # 등록일
                registration_date = detail_link_connect[2]
                registration_date = registration_date.replace('.', '/')

                # primary key
                modify_title = re.sub('[^A-Za-z0-9가-힣]', '', detail_link_connect[0])
                modify_recruiter = re.sub('[^A-Za-z0-9가-힣]', '', recruiter)
                split_workplace = workplace.split('\n')
                modify_workplace = re.sub('[^A-Za-z0-9가-힣]', '', split_workplace[0])
                primary_key = "E" + str(modify_title) + "#" + str(modify_recruiter) + "#" + str(modify_workplace)

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
                    'business_hours': business_hours + " " + business_form,
                    'recruiter': recruiter,
                    'contact_address': contact_address,
                    'registration_date': registration_date,
                    'primary_key': primary_key
                }

                announcement_list_Seoul_Eunpyeong.append(data)

            except NoSuchElementException:
                pass

    return announcement_list_Seoul_Eunpyeong


def pass_the_next_link(driver, url, index):
    if index < 1:
        driver.get(url)
        next_link = driver.find_element(By.XPATH, '//*[@id="awdDisplayContent"]/div/div[2]/a[1]').get_attribute(
            'href')
    else:
        driver.get(url)
        next_link = driver.find_element(By.XPATH, '//*[@id="awdDisplayContent"]/div/div[2]/a[2]').get_attribute(
            'href')

    return next_link


def main(driver):
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'http://www.epsjcenter.or.kr/main/sub.html?boardID=www7&keyfield=&key='

    # 웹드라이버 열기
    # options=options 추가해주기
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(3)

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Seoul_Eunpyeong = []

    index = 0
    while index < 4:
        notices = approach_the_list(driver)
        detail_link_list = extract_url(notices)
        announcement_list_Seoul_Eunpyeong = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Seoul_Eunpyeong)

        next_link = pass_the_next_link(driver, url, index)

        url = next_link
        driver.get(next_link)
        index = index + 1

    driver.close()
    driver.quit()

    return announcement_list_Seoul_Eunpyeong
