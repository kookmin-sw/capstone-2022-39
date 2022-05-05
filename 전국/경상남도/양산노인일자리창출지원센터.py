# selenium Ver : 3.14.1
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from openpyxl import Workbook

# 통합문서 열기
xlsx = Workbook()


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(steady_number, index):
    title_name_and_detail_link_list = list()  # 제목 및 상세 페이지를 위한 URL 수집

    time.sleep(3)
    index_url = index * 10
    for i in range(0, 10):
        try:
            steady_url = "https://yangsansj.or.kr/yss/work/w03_dtl.do?pNum="

            detail_link = steady_url + str(steady_number - index_url + 9)

            title_name_and_detail_link_list.append([detail_link])
        except NoSuchElementException:
            pass

        index_url = index_url + 1

    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list):
    detail_page_text = list()

    time.sleep(1)
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.get(str(detail_link_connect[0]))
        time.sleep(5)

        section = driver.find_element(By.XPATH,
                                      '//*[@id="container"]/div[2]/div[1]/table/tbody/tr[1]/td').text

        if section.__contains__("모집중"):

            detail_title = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/table/tbody/tr[1]/td').text

            # 근무지 추출
            workplace = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/table/tbody/tr['
                                                      '4]/td/div/table/tbody/tr[2]/td[1]').text

            # 모집 인원 추출
            recruitment_staff = driver.find_element(By.XPATH,
                                                    '//*[@id="container"]/div[2]/div[1]/table/tbody/tr['
                                                    '4]/td/div/table/tbody/tr[2]/td[2]').text

            # 성별 추출
            gender = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/table/tbody/tr['
                                                   '4]/td/div/table/tbody/tr[3]/td[2]').text

            # 연령 추출
            age = driver.find_element(By.XPATH,
                                      '//*[@id="container"]/div[2]/div[1]/table/tbody/tr[4]/td/div/table/tbody/tr['
                                      '3]/td[1]').text

            # 모집 분야 추출
            if detail_title.__contains__("미화"):
                recruitment_field = "환경미화"
            elif detail_title.__contains__("경비"):
                recruitment_field = "경비"
            elif detail_title.__contains__("주차"):
                recruitment_field = "주차관리원"
            elif detail_title.__contains__("주방") or detail_title.__contains__("조리"):
                recruitment_field = "주방보조원"
            elif detail_title.__contains__("생산") or detail_title.__contains__("제조"):
                recruitment_field = "생산/제조"
            elif detail_title.__contains__("운전"):
                recruitment_field = "운전원"
            elif detail_title.__contains__("노무"):
                recruitment_field = "일반단순노무직"
            else:
                recruitment_field = "기타"

            # 우대 사항 추출
            qualification_license = '-'
            # 내용 추출
            job_specifications = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/table/tbody/tr['
                                                               '4]/td/div/table/tbody/tr[6]/td/div').text

            # 고용 형태 추출
            employment = '-'

            # 급여액 추출
            wages = driver.find_element(By.XPATH,
                                        '//*[@id="container"]/div[2]/div[1]/table/tbody/tr[4]/td/div/table/tbody/tr['
                                        '4]/td[2]').text

            # 근무 시간 추출
            business_hours = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/table/tbody/tr['
                                                           '4]/td/div/table/tbody/tr[5]/td').text

            # 채용 담당자 추출
            recruiter = "양산노인일자리창출지원센터 "

            # 연락처 추출
            contact_address = "전화문의 055)392-5651~3"

            detail_page_text.append(
                [detail_title, detail_link_connect[0], workplace, recruitment_staff + "/" + gender + "/" + age,
                 recruitment_field, qualification_license, job_specifications, employment, wages, business_hours,
                 recruiter, contact_address])

    return detail_page_text


def pass_the_next_link():
    links = list()
    url = "https://yangsansj.or.kr/yss/work/w03.do?searchCondition=&searchKeyword=&pageIndex="
    for i in range(2, 3):
        links.append(url + str(i))

    return links


def main():
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'https://yangsansj.or.kr/yss/work/w03.do'

    # 웹드라이버 열기
    # options=options 추가해주기
    driver = webdriver.Chrome('C:/chromedriver.exe')
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(3)

    # 시트 만들기
    xlsx.create_sheet("양산노인일자리창출지원센터")
    sheet = xlsx["양산노인일자리창출지원센터"]
    sheet.append(['제목', 'URL', '근무지', '모집인원', '모집분야', '우대사항',
                  '내용', '고용형태', '급여액', '근무시간', '채용담당자',
                  '연락처'])

    # 링크  추출
    next_link = pass_the_next_link()

    # 페이지마다 고정적인 번호 추출
    steady_number = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[2]/table/tbody/tr[1]/td[1]').text
    index = 0
    for link in next_link:
        detail_link_list = extract_url(int(steady_number), index)
        detail_page_text = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list)
        for page_text in detail_page_text:
            sheet.append(page_text)

        driver.get(link)
        index = index + 1
        time.sleep(2)

    del xlsx['Sheet']  # 기본 시트 삭제
    filename = "C:/Python/" + "양산노인일자리창출지원센터" + "_NewList.xlsx"
    xlsx.save(filename)  # 통합문서 저장
    xlsx.close()  # 통합문서 종료

    driver.close()
    driver.quit()


main()
