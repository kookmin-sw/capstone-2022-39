"""
- selenium Ver : 3.14.1
- 사)대한노인회전북취업지원센터
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from wholeCountry.areas_of_recruitment import areas_of_recruitment
import re


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    time.sleep(3)
    notices = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div/form[1]/table[2]/tbody') \
        .find_elements(By.TAG_NAME, 'tr')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices):
    # 제목 및 상세 페이지를 위한 URL 수집
    title_name_and_detail_link_list = list()
    time.sleep(1)

    for notice in notices:
        detail = notice.find_elements(By.CLASS_NAME, 'vdb_line')
        detail_title = detail[1].text
        detail_link = detail[1].find_element(By.TAG_NAME, 'a') \
            .get_attribute('href')

        registration_date = detail[5].text

        title_name_and_detail_link_list.append([detail_title, detail_link, registration_date[2:10]])

    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Jeonbuk_Jeonbuk_ency):
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.get(str(detail_link_connect[1]))

        time.sleep(1)

        section_check = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div/table['
                                                      '3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td').text
        if section_check != "모집중" or detail_link_connect[0].__contains__("마감"):
            pass
        else:
            # 근무지 추출
            workplace = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div/table['
                                                      '3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td').text

            # 모집 인원 추출
            recruitment_staff = '-명'

            # 성별 추출
            gender = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div/table['
                                                   '3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[5]/td').text

            # 연령 추출
            age = driver.find_element(By.XPATH,
                                      '//*[@id="contentBox"]/div/table['
                                      '3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td').text

            # 우대 사항 추출
            qualification_license = '-'

            # 내용 추출
            job_specifications = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div/table['
                                                               '3]/tbody/tr/td/table/tbody/tr/td/div').text

            # 고용 형태 추출
            employment = '-'

            # 급여액 추출
            wages = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div/table['
                                                  '3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[6]/td').text

            # 근무 시간 추출
            business_hours = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div/table['
                                                           '3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr['
                                                           '7]/td').text

            # 채용 담당자 추출
            recruiter = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div/table['
                                                      '3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[8]/td').text

            # 연락처 추출
            contact_address = '063-273-2086'

            # 등록일
            registration_date = detail_link_connect[2]

            # 모집 분야
            recruitment_field = areas_of_recruitment(detail_link_connect[0] + job_specifications)

            # primary key
            modify_title = re.sub('[^A-Za-z0-9가-힣]', '', detail_link_connect[0])
            modify_recruiter = re.sub('[^A-Za-z0-9가-힣]', '', recruiter)
            modify_workplace = re.sub('[^A-Za-z0-9가-힣]', '', workplace)
            primary_key = "JE" + str(modify_title) + "#" + str(modify_recruiter) + "#" + str(modify_workplace)

            data = {
                'title': detail_link_connect[0],
                'url': detail_link_connect[1],
                'workplace': workplace,
                'recruitment_staff': recruitment_staff+"/"+age+"/"+gender,
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

            announcement_list_Jeonbuk_Jeonbuk_ency.append(data)

    return announcement_list_Jeonbuk_Jeonbuk_ency


def pass_the_next_link(driver):
    next_link = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div/table/tbody/tr/td')\
        .find_elements(By.TAG_NAME, 'a')
    return next_link


def main(driver):
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'http://www.jbsjob.or.kr/board/56'

    # 웹드라이버 열기
    # options=options 추가해주기
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(3)

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Jeonbuk_Jeonbuk_ency = []

    next_link = pass_the_next_link(driver)
    detail_link = list()
    for i in range(len(next_link)):
        detail_link.append(next_link[i].get_attribute('href'))

    index = 0
    while index < len(next_link) - 6:
        notices = approach_the_list(driver)
        detail_link_list = extract_url(notices)
        announcement_list_Jeonbuk_Jeonbuk_ency = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Jeonbuk_Jeonbuk_ency)

        driver.get(detail_link[index])
        index = index + 1
        time.sleep(1)

    return announcement_list_Jeonbuk_Jeonbuk_ency
