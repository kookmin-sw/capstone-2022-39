"""
- selenium Ver : 3.14.1
- 양산노인일자리창출지원센터
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from wholeCountry.areas_of_recruitment import areas_of_recruitment
from datetime import datetime


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


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Gyeongnam_Yangsan):
    now = datetime.now()
    time.sleep(1)
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.get(str(detail_link_connect[0]))
        time.sleep(2)

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
            recruitment_field = areas_of_recruitment(detail_title)

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

            # primary key
            primary_key = "B" + str(now.time())

            data = {
                'title': detail_title,
                'url': detail_link_connect[0],
                'workplace': workplace,
                'recruitment_staff': recruitment_staff + "/" + gender + "/" + age,
                'recruitment_field': recruitment_field,
                'qualification_license': qualification_license,
                'job_specifications': job_specifications,
                'employment': employment,
                'wages': wages,
                'business_hours': business_hours,
                'recruiter': recruiter,
                'contact_address': contact_address,
                'primary_key': primary_key
            }

            announcement_list_Gyeongnam_Yangsan.append(data)

    return announcement_list_Gyeongnam_Yangsan


def pass_the_next_link():
    links = list()
    url = "https://yangsansj.or.kr/yss/work/w03.do?searchCondition=&searchKeyword=&pageIndex="
    for i in range(2, 5):
        links.append(url + str(i))

    return links


def main(driver):
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'https://yangsansj.or.kr/yss/work/w03.do'

    # 웹드라이버 열기
    # options=options 추가해주기
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(3)

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Gyeongnam_Yangsan = []

    # 링크  추출
    next_link = pass_the_next_link()

    # 페이지마다 고정적인 번호 추출
    steady_number = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[2]/table/tbody/tr[1]/td[1]').text
    index = 0
    for link in next_link:
        detail_link_list = extract_url(int(steady_number), index)
        announcement_list_Gyeongnam_Yangsan = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Gyeongnam_Yangsan)

        driver.get(link)
        index = index + 1
        time.sleep(3)

    return announcement_list_Gyeongnam_Yangsan
