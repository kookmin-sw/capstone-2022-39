"""
- selenium Ver : 3.14.1
- 전북노인일자리센터
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from wholeCountry.areas_of_recruitment import areas_of_recruitment
import re
import datetime


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    time.sleep(3)
    notices = driver.find_element(By.CLASS_NAME, 'tbl_head01.tbl_wrap')\
        .find_element(By.TAG_NAME, 'tbody')\
        .find_elements(By.TAG_NAME, 'tr')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices):
    # 제목 및 상세 페이지를 위한 URL 수집
    title_name_and_detail_link_list = list()
    time.sleep(1)

    for notice in notices:
        check = notice.find_element(By.CLASS_NAME, 'td_datetime').text
        if check == "채용완료":
            pass
        else:
            detail = notice.find_element(By.CLASS_NAME, 'bo_tit')

            detail_title = detail.text
            detail_link = detail.find_element(By.TAG_NAME, 'a')\
                .get_attribute('href')

            registration_date = notice.find_elements(By.CLASS_NAME, 'td_datetime')[1].text
            registration_date = registration_date.replace('-', '/')

            title_name_and_detail_link_list.append([detail_title, detail_link, registration_date])

    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Jeonbuk_Jeonbuk):
    today = datetime.date.today()
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.get(str(detail_link_connect[1]))
        time.sleep(1)

        # 근무지 추출
        workplace = driver.find_element(By.XPATH, '//*[@id="bo_v_atc"]/div/table/tbody/tr[6]/td/span').text

        # 모집 인원 추출
        recruitment_staff = driver.find_element(By.XPATH, '//*[@id="bo_v_atc"]/div/table/tbody/tr[8]/td[1]').text

        # 성별 추출
        # gender = driver.find_element(By.XPATH, '//*[@id="contentBox"]/table['
        #                                        '3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[5]/td').text

        # 연령 추출
        age = driver.find_element(By.XPATH,
                                  '//*[@id="bo_v_atc"]/div/table/tbody/tr[8]/td[2]').text

        # 우대 사항 추출
        qualification_license = driver.find_element(By.XPATH, '//*[@id="bo_v_atc"]/div/table/tbody/tr[13]/td').text
        if len(qualification_license) <= 2:
            qualification_license = '-'

        # 내용 추출
        job_specifications = driver.find_element(By.XPATH, '//*[@id="bo_v_con"]').text

        # 고용 형태 추출
        employment = driver.find_element(By.XPATH, '//*[@id="bo_v_atc"]/div/table/tbody/tr[7]/td[1]').text

        # 급여액 추출
        wages = driver.find_element(By.XPATH, '//*[@id="bo_v_atc"]/div/table/tbody/tr[7]/td[2]').text

        # 근무 시간 추출
        business_hours = driver.find_element(By.XPATH, '//*[@id="bo_v_atc"]/div/table/tbody/tr[9]/td').text

        # 지원 센터 추출
        center = "전북노인일자리센터"

        # 채용 담당자 추출
        recruiter = driver.find_element(By.XPATH, '//*[@id="bo_v_atc"]/div/table/tbody/tr[16]/td').text

        # 연락처 추출
        contact_address = driver.find_element(By.XPATH, '//*[@id="bo_v_atc"]/div/table/tbody/tr[17]/td').text

        # 등록일
        registration_date = "22/" + detail_link_connect[2]

        # 모집 분야
        recruitment_field = areas_of_recruitment(detail_link_connect[0] + job_specifications)

        if registration_date[5:6] == ":":
            month = today.month
            day = today.day
            if int(month) < 10 and int(day) < 10:
                registration_date = "22/0" + str(month) + "/0" + str(day)
            elif int(month) > 10 and int(day) < 10:
                registration_date = "22/" + str(month) + "/0" + str(day)
            elif int(month) < 10 and int(day) > 10:
                registration_date = "22/0" + str(month) + "/" + str(day)
            else:
                registration_date = "22/" + str(month) + "/" + str(day)

        # primary key
        modify_title = re.sub('[^A-Za-z0-9가-힣]', '', detail_link_connect[0])
        modify_recruiter = re.sub('[^A-Za-z0-9가-힣]', '', recruiter)
        modify_workplace = re.sub('[^A-Za-z0-9가-힣]', '', workplace)
        primary_key = "JB" + str(modify_title) + "#" + str(modify_recruiter) + "#" + str(modify_workplace)

        data = {
            'title': detail_link_connect[0],
            'url': detail_link_connect[1],
            'workplace': workplace,
            'recruitment_staff': recruitment_staff+"/"+age,
            'recruitment_field': recruitment_field,
            'qualification_license': qualification_license,
            'job_specifications': job_specifications,
            'employment': employment,
            'wages': wages,
            'business_hours': business_hours,
            'recruiter': center,
            'contact_address': recruiter + " " + contact_address[0:12],
            'registration_date': registration_date,
            'primary_key': primary_key
        }

        announcement_list_Jeonbuk_Jeonbuk.append(data)

    return announcement_list_Jeonbuk_Jeonbuk


def pass_the_next_link(driver):
    next_link = driver.find_element(By.CLASS_NAME, 'pg')\
        .find_elements(By.TAG_NAME, 'a')
    return next_link


def main(driver):
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'http://www.jbsilver.net/bbs/board.php?bo_table=sub04_01'

    # 웹드라이버 열기
    # options=options 추가해주기
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(3)

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Jeonbuk_Jeonbuk = []

    next_link = pass_the_next_link(driver)
    detail_link = list()
    for i in range(len(next_link)):
        detail_link.append(next_link[i].get_attribute('href'))

    index = 0
    while index < len(next_link) - 2:
        notices = approach_the_list(driver)
        detail_link_list = extract_url(notices)
        announcement_list_Jeonbuk_Jeonbuk = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Jeonbuk_Jeonbuk)

        driver.get(detail_link[index])
        index = index + 1
        time.sleep(1)

    return announcement_list_Jeonbuk_Jeonbuk

