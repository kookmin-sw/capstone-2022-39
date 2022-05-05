# selenium Ver : 3.14.1
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from openpyxl import Workbook

# 통합문서 열기
xlsx = Workbook()


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
            if detail_title.__contains__("#"):
                title_name_and_detail_link_list.append([detail_title[5:], detail_link])
            else:
                title_name_and_detail_link_list.append([detail_title, detail_link])

    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list):
    detail_page_text = list()
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.get(str(detail_link_connect[1]))

        time.sleep(3)
        section_check = driver.find_element(By.XPATH, '//*[@id="AB_viewPrintArea"]/ul/li[1]/div/ul/span').text
        # print(section_check)

        if section_check == "[구인중]":
            # 근무지 추출
            workplace = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[1]/tbody/tr[2]/td['
                                                      '5]/span/strong/span').text

            # 모집인원 추출
            recruitment_staff = driver.find_element(By.XPATH,
                                                    '//*[@id="lightgallery"]/table[1]/tbody/tr[2]/td['
                                                    '4]/span/strong/span').text

            # 모집 분야 추출
            if detail_link_connect[0].__contains__("미화"):
                recruitment_field = "환경미화"
            elif detail_link_connect[0].__contains__("경비"):
                recruitment_field = "경비"
            elif detail_link_connect[0].__contains__("주차"):
                recruitment_field = "주차관리원"
            elif detail_link_connect[0].__contains__("주방") or detail_link_connect[0].__contains__("조리"):
                recruitment_field = "주방보조원"
            elif detail_link_connect[0].__contains__("생산") or detail_link_connect[0].__contains__("제조"):
                recruitment_field = "생산/제조"
            elif detail_link_connect[0].__contains__("운전"):
                recruitment_field = "운전원"
            elif detail_link_connect[0].__contains__("노무"):
                recruitment_field = "일반단순노무직"
            else:
                recruitment_field = "기타"

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
            wages = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[2]/tbody/tr[2]/td[1]/span/strong/span').text

            # 근무 시간 추출
            business_hours = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[2]/tbody/tr[2]/td['
                                                           '2]/div/span/strong/span/span').text
            try:
                business_form = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[2]/tbody/tr[2]/td['
                                                              '3]/span/strong/span').text
            except NoSuchElementException:
                business_form = driver.find_element(By.XPATH, '//*[@id="lightgallery"]/table[2]/tbody/tr[2]/td[3]/span').text

            # 채용 담당자 추출
            recruiter = "서울특별시 은평구 증산로 23길 7, 4층"

            # 연락처 추출
            contact_address = "070-7728-2807"

            detail_page_text.append([detail_link_connect[0], detail_link_connect[1], workplace, recruitment_staff,
                                    recruitment_field, qualification_license, job_specifications, employment,
                                     wages, business_hours + " " + business_form,
                                     recruiter, contact_address])

    return detail_page_text


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


def main():
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'http://www.epsjcenter.or.kr/main/sub.html?boardID=www7&keyfield=&key='

    # 웹드라이버 열기
    # options=options 추가해주기
    driver = webdriver.Chrome('C:/chromedriver.exe')
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(5)

    # 시트 만들기
    xlsx.create_sheet("은평어르신일자리센터")
    sheet = xlsx["은평어르신일자리센터"]
    sheet.append(['제목', 'URL', '근무지', '모집인원', '모집분야', '우대사항',
                  '내용', '고용형태', '급여액', '근무시간', '채용담당자',
                  '연락처'])

    index = 0
    while index < 5:
        notices = approach_the_list(driver)
        detail_link_list = extract_url(notices)
        detail_page_text = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list)

        for link_list, page_text in zip(detail_link_list, detail_page_text):
            sheet.append(page_text)

        next_link = pass_the_next_link(driver, url, index)

        url = next_link
        driver.get(next_link)
        index = index + 1

    del xlsx['Sheet']  # 기본 시트 삭제
    filename = "C:/Python/" + "은평어르신일자리센터" + "_NewList.xlsx"
    xlsx.save(filename)  # 통합문서 저장
    xlsx.close()  # 통합문서 종료

    driver.close()
    driver.quit()


main()
