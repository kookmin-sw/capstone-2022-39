"""
- selenium Ver : 3.14.1
- 양산노인일자리창출지원센터
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from wholeCountry.areas_of_recruitment import areas_of_recruitment
import re


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    notices = driver.find_element(By.CLASS_NAME, 't-list') \
        .find_element(By.TAG_NAME, 'tbody') \
        .find_elements(By.TAG_NAME, 'tr')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices):
    title_name_and_detail_link_list = list()  # 제목 및 상세 페이지를 위한 URL 수집

    time.sleep(3)
    for notice in notices:
        try:

            detail_title = notice.find_elements(By.TAG_NAME, 'td')[1].text

            detail_link = notice.find_element(By.TAG_NAME, 'a').get_attribute('href')

            registration_date = notice.find_elements(By.TAG_NAME, 'td')[3].text
            registration_date = registration_date.replace('-', '/')

            title_name_and_detail_link_list.append([detail_title, detail_link, registration_date[2:10]])
        except NoSuchElementException:
            pass

    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Gyeongnam_Yangsan):
    time.sleep(1)
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.get(str(detail_link_connect[1]))
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

            # 등록일
            registration_date = detail_link_connect[2]

            # primary key
            modify_title = re.sub('[^A-Za-z0-9가-힣]', '', detail_link_connect[0])
            modify_recruiter = re.sub('[^A-Za-z0-9가-힣]', '', recruiter)
            modify_workplace = re.sub('[^A-Za-z0-9가-힣]', '', workplace)
            primary_key = "Y" + str(modify_title) + "#" + str(modify_recruiter) + "#" + str(modify_workplace)

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
                'registration_date': registration_date,
                'primary_key': primary_key
            }

            announcement_list_Gyeongnam_Yangsan.append(data)

    return announcement_list_Gyeongnam_Yangsan


def pass_the_next_link():
    links = list()
    url = "https://yangsansj.or.kr/yss/work/w03.do?searchCondition=&searchKeyword=&pageIndex="
    for i in range(2, 4):
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

    for link in next_link:
        notices = approach_the_list(driver)
        detail_link_list = extract_url(notices)
        announcement_list_Gyeongnam_Yangsan = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Gyeongnam_Yangsan)

        driver.get(link)
        time.sleep(3)

    return announcement_list_Gyeongnam_Yangsan
