"""
- 노인일자리여기
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException
import time
from openpyxl import Workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wholeCountry.areas_of_recruitment import areas_of_recruitment

# 통합문서 열기
# xlsx = Workbook()


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    time.sleep(3)
    notices_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'rsList02')))
    notices = WebDriverWait(notices_list, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))
    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices):
    title_name_and_detail_link_list = list()  # 제목 및 상세 페이지를 위한 URL 수집

    time.sleep(5)
    for notice in notices:
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
            section = WebDriverWait(notice, 10, ignored_exceptions=ignored_exceptions) \
                .until(EC.presence_of_element_located((By.CLASS_NAME, 'badge-info')))
            if section.text == "접수중":
                detail_title = notice.find_element(By.CLASS_NAME, 'info-tit').text
                # print("[" + detail_title + "]")
                detail_link = notice.find_element(By.CLASS_NAME, 'info').find_element(By.TAG_NAME, 'a').get_attribute(
                    'href')
                # print("[" + detail_link + "]")

                title_name_and_detail_link_list.append([detail_title, detail_link])
        except NoSuchElementException:
            pass
    # print("---")
    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Here):
    detail_page_text = list()
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.execute_script(detail_link_connect[1])
        time.sleep(5)

        # 근무지 추출
        workplace = driver.find_element(By.XPATH, '//*[@id="dDtlWorkArea"]').text
        # 모집 인원 추출
        recruitment_staff = driver.find_element(By.XPATH,
                                                '//*[@id="dWokerCnt"]').text

        # 모집 분야 추출
        recruitment_field = areas_of_recruitment(detail_link_connect[0])

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
            'contact_address': contact_address
        }

        announcement_list_Here.append(data)

        detail_page_text.append(
            [detail_link_connect[0], detail_link_connect[1], workplace, recruitment_staff,
             recruitment_field, qualification_license, job_specifications, employment,
             wages, business_hours, recruiter, contact_address])

    return detail_page_text, announcement_list_Here


def pass_the_next_link(driver):
    links_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'paging02')))
    links = WebDriverWait(links_list, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))

    return links


def main(driver):
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'https://www.seniorro.or.kr:4431/seniorro/main/main.do'
    # 웹드라이버 열기
    # options=options 추가해주기
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 5초까지 기다려 준다.
    # driver.implicitly_wait(5)
    time.sleep(5)

    # 지속적으로 홈페이지에 오류가 나서 새로고침을 하도록 함.
    driver.refresh()
    time.sleep(3)

    # 시트 만들기
    # xlsx.create_sheet("노인일자리여기")
    # sheet = xlsx["노인일자리여기"]
    # sheet.append(['제목', 'URL', '근무지', '모집인원', '모집분야', '우대사항',
    #               '내용', '고용형태', '급여액', '근무시간', '채용담당자',
    #               '연락처'])

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Here = []

    # 일자리여기 검색창 Xpath
    xpath_text = '//*[@id="seachKeyword"]'
    # 검색하기 버튼
    xpath_button = '//*[@id="container_wr"]/div[1]/div[3]/button/i'

    # 지리 리스트
    f = open(r"C:\Users\Admin\Documents\GitHub\capstone-2022-39\wholeCountry\w_Country\district.txt", 'r', encoding="cp949")

    while True:
        keyword = f.readline()

        # 검색 창에 keyword 입력
        driver.refresh()
        time.sleep(3)
        driver.find_element(By.XPATH, xpath_text).send_keys(keyword)
        time.sleep(5)
        # 검색 버튼 클릭하기
        try:
            driver.find_element(By.XPATH, xpath_button).click()
            time.sleep(3)
        except ElementClickInterceptedException:
            pass

        next_link = pass_the_next_link(driver)
        detail_link_list = list()
        for i in range(2, len(next_link) - 1):
            detail_link_list.append(next_link[i].get_attribute('href'))

        for detail_link in detail_link_list:
            try:
                notices = approach_the_list(driver)
                detail_link_list = extract_url(notices)
                detail_page_text, announcement_list_Here = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Here)

                # for link_list, page_text in zip(detail_link_list, detail_page_text):
                #     sheet.append(page_text)

                # print(detail_link)
                driver.execute_script(detail_link)
            except NoSuchElementException:
                pass
        time.sleep(5)
        if not keyword:
            break
        driver.get(url)
    f.close()

    # del xlsx['Sheet']  # 기본 시트 삭제
    # filename = "C:/Python/" + "노인일자리여기" + "_NewList.xlsx"
    # xlsx.save(filename)  # 통합문서 저장
    # xlsx.close()  # 통합문서 종료

    driver.close()
    driver.quit()

    return announcement_list_Here
