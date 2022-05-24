"""
- selenium Ver : 3.14.1
- 50+부산포털
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
import time
from wholeCountry.areas_of_recruitment import areas_of_recruitment
import re
import datetime


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    notices = driver.find_element(By.ID, 'idNomalTableList') \
        .find_element(By.TAG_NAME, 'tbody') \
        .find_elements(By.TAG_NAME, 'tr')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices, link_list):
    for notice in notices:
        time.sleep(2)
        try:
            # 구인제목 추출
            detail_title = notice.find_element(By.CLASS_NAME, 'title').text

            # a href 태그에 있는 URL 추출
            detail_link = notice.find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME, 'a').get_attribute(
                'href')
            registration_date = notice.find_element(By.CLASS_NAME, 'upload.last').text

            link_list.append([detail_title, detail_link, registration_date])

        except NoSuchElementException:
            pass

    return link_list


# 공고의 정보를 담고 있는 URL를 접속하여 추출
def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_FleaMarket):
    today = datetime.date.today()
    for detail_link_connect in detail_link_list:
        time.sleep(3)
        try:
            driver.get(detail_link_connect[1])
        except WebDriverException:
            pass

        # 근무지 추출
        try:
            workplace = driver.find_element(By.ID, 'work_place').text
        except NoSuchElementException:
            workplace = driver.find_element(By.CLASS_NAME, 'current').text

        # 모집인원 추출
        recruitment_staff = '-명'

        # 자격 면허 추출
        qualification_license = '-'

        # 내용 추출
        job_specifications = '-'

        # 고용 형태 추출
        employment = '-'

        # 급여액 추출
        wage_time = driver.find_element(By.CLASS_NAME, 'pay').find_element(By.ID, 'pay_title').text
        wages = driver.find_element(By.CLASS_NAME, 'pay').find_element(By.ID, 'pay_num').text

        # 근무시간 추출
        try:
            business_date = driver.find_element(By.CLASS_NAME, 'date').find_element(By.CLASS_NAME, 'work_date').text
        except NoSuchElementException:
            business_date = '-'

        try:
            business_day = driver.find_element(By.CLASS_NAME, 'time').find_element(By.CLASS_NAME, 'title').text
        except NoSuchElementException:
            business_day = '-'

        try:
            business_hours = driver.find_element(By.CLASS_NAME, 'time').find_element(By.CLASS_NAME, 'num').text
        except NoSuchElementException:
            business_hours = '-'

        # 채용담당자 추출
        recruiter = '-'

        # 연락처 추출
        contact_address = '-'
        represent_address = '-'

        working_conditions = driver.find_element(By.CLASS_NAME, 'work').find_element(By.CLASS_NAME, 'con_list').find_elements(By.TAG_NAME, 'li')
        for condition in working_conditions:
            try:
                if condition.find_element(By.CLASS_NAME, 'tit').text == "근무유형":
                    employment = condition.find_element(By.CLASS_NAME, 'info.btn_plus').text
                elif condition.find_element(By.CLASS_NAME, 'tit').text == "담당업무":
                    job_specifications = condition.find_element(By.CLASS_NAME, 'info.btn_plus').text
            except NoSuchElementException:
                pass

        qualifications = driver.find_element(By.CLASS_NAME, 'qualification').find_element(By.CLASS_NAME, 'con_list').find_elements(By.TAG_NAME, 'li')
        for qualification in qualifications:
            try:
                if qualification.find_element(By.CLASS_NAME, 'tit').text == "우대/가능":
                    qualification_license = qualification.find_element(By.CLASS_NAME, 'info.plus.btn_plus').text
            except NoSuchElementException:
                pass

        company_info = driver.find_element(By.CLASS_NAME, 'period_box').find_element(By.CLASS_NAME, 'company_info').find_elements(By.TAG_NAME, 'li')
        for info in company_info:
            try:
                if info.find_element(By.CLASS_NAME, 'tit').text == "모집인원":
                    recruitment_staff = info.find_element(By.CLASS_NAME, 'con.num').text
                elif info.find_element(By.CLASS_NAME, 'tit').text == "채용 담당자":
                    recruiter = info.find_element(By.CLASS_NAME, 'con').text
                elif info.find_element(By.CLASS_NAME, 'tit').text == "담당자 전화":
                    contact_address = info.find_element(By.CLASS_NAME, 'con.num').text
                elif info.find_element(By.CLASS_NAME, 'tit').text == "대표 전화":
                    represent_address = info.find_element(By.CLASS_NAME, 'con.num').text
                else:
                    pass
            except NoSuchElementException:
                pass

        # 모집 분야
        recruitment_field = areas_of_recruitment(detail_link_connect[0] + job_specifications)

        if recruiter == '-':
            recruiter = "벼룩시장"

        # 등록일
        registration_date = detail_link_connect[2]

        if registration_date.__contains__("분전"):
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
        else:
            registration_date = "22/" + detail_link_connect[2]

        # primary key
        modify_title = re.sub('[^A-Za-z0-9가-힣]', '', detail_link_connect[0])
        modify_recruiter = re.sub('[^A-Za-z0-9가-힣]', '', recruiter)
        modify_workplace = re.sub('[^A-Za-z0-9가-힣]', '', workplace)
        primary_key = "B" + str(modify_title) + "#" + str(modify_recruiter) + "#" + str(modify_workplace)

        data = {
            'title': detail_link_connect[0],
            'url': detail_link_connect[1],
            'workplace': workplace,
            'recruitment_staff': recruitment_staff,
            'recruitment_field': recruitment_field,
            'qualification_license': qualification_license,
            'job_specifications': job_specifications,
            'employment': employment,
            'wages': wage_time + " " + wages,
            'business_hours': business_date + "/" + business_day + "/" + business_hours,
            'recruiter': recruiter,
            'contact_address': contact_address + " " + represent_address,
            'registration_date': registration_date,
            'primary_key': primary_key
        }

        announcement_list_FleaMarket.append(data)

    return announcement_list_FleaMarket


def main(driver):
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'http://www.findjob.co.kr/job/category/specialistDetailJob.asp?Page=1&SpID=1015&TotalCount=7214&sltAreaA=&sltAreaB=&sltAreaC=&sltFindCodeA=&sltFindCodeB=&sltFindCodeC=&DayWeek=0&DayWeekNego=0&Time=0&TimeFrom=0&TimeTo=0&TimeNego=0&WorkMain=0&WorkSub=0&WorkOut=0&PartTimeF=0&WorkAppoint=0&WorkFreelancer=0&PayF=0&PayForm=0&PayPossible=0&PayType1=0&PayType2=0&PayType3=0#Normal'
    # 웹드라이버 열기
    # options=options 추가해주기
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(1)

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_FleaMarket = []

    steady_url = "http://www.findjob.co.kr/job/category/specialistDetailJob.asp?Page="
    end_url = "&SpID=1015&TotalCount=7214&sltAreaA=&sltAreaB=&sltAreaC=&sltFindCodeA=&sltFindCodeB=&sltFindCodeC=&DayWeek=0&DayWeekNego=0&Time=0&TimeFrom=0&TimeTo=0&TimeNego=0&WorkMain=0&WorkSub=0&WorkOut=0&PartTimeF=0&WorkAppoint=0&WorkFreelancer=0&PayF=0&PayForm=0&PayPossible=0&PayType1=0&PayType2=0&PayType3=0#Normal"

    fields = driver.find_elements(By.TAG_NAME, 'input')
    for field in fields:
        # 눈에 보이는지 확인
        if not field.is_displayed():
            print("this input is a trap :" + field.get_attribute("id"))

    link_list = list()
    index = 2
    while index < 4:
        notices = approach_the_list(driver)
        extract_url(notices, link_list)
        driver.get(steady_url + str(index) + end_url)
        time.sleep(3)
        index = index + 1

    announcement_list_FleaMarket = approach_detail_link_and_extract_recruitment_info(driver, link_list, announcement_list_FleaMarket)

    return announcement_list_FleaMarket
