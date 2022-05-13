"""
- selenium Ver : 3.14.1
- 50+부산포털
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from openpyxl import Workbook
from wholeCountry.areas_of_recruitment import areas_of_recruitment

# 통합문서 열기
xlsx = Workbook()


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    notices = driver.find_element(By.CLASS_NAME, 'list_table') \
        .find_element(By.TAG_NAME, 'tbody') \
        .find_elements(By.TAG_NAME, 'tr')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices):
    detail_link_list = list()

    for notice in notices:
        # 구인제목 추출
        detail_title = notice.find_element(By.CLASS_NAME, 'title.jc02').find_element(By.CLASS_NAME, 'job_title').text

        # a href 태그에 있는 URL 추출
        detail_link = notice.find_element(By.CLASS_NAME, 'title.jc02').find_element(By.TAG_NAME, 'a').get_attribute(
            'href')

        detail_link_list.append([detail_title, detail_link])

    return detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, sheet, announcement_list_Busan_Busan):
    for detail_link_connect in detail_link_list:
        driver.get(detail_link_connect[1])

        # 근무지 추출
        workplace = driver.find_element(By.XPATH, '//*[@id="job_container"]/div[6]/table/tbody/tr[1]/td').text

        # 모집인원 추출
        recruitment_staff = driver.find_element(By.XPATH,
                                                '//*[@id="job_container"]/div[6]/table/tbody/tr[2]/td[1]').text

        # 성별 추출
        gender = driver.find_element(By.XPATH, '//*[@id="job_container"]/div[6]/table/tbody/tr[2]/td[2]').text

        # 연령 추출
        age = driver.find_element(By.XPATH, '//*[@id="job_container"]/div[6]/table/tbody/tr[3]/td[1]').text

        # 모집 분야
        recruitment_field = areas_of_recruitment(detail_link_connect[0])

        # 자격 면허 추출
        qualification_license = driver.find_element(By.XPATH,
                                                    '//*[@id="job_container"]/div[6]/table/tbody/tr[4]/td[2]').text

        # 내용 추출
        job_specifications = driver.find_element(By.XPATH, '//*[@id="job_container"]/div[6]/table/tbody/tr[6]/td').text

        # 고용 형태 추출
        employment = driver.find_element(By.XPATH, '//*[@id="job_container"]/div[6]/table/tbody/tr[8]/td').text

        # 급여액 추출
        wages = driver.find_element(By.XPATH, '//*[@id="job_container"]/div[6]/table/tbody/tr[10]/td').text

        # 근무시간 추출
        business_hours = driver.find_element(By.XPATH, '//*[@id="job_container"]/div[6]/table/tbody/tr[12]/td').text

        # 채용담당자 추출
        recruiter = driver.find_element(By.XPATH, '//*[@id="job_container"]/div[7]/table/tbody/tr[1]/td').text

        # 연락처 추출
        contact_address = driver.find_element(By.XPATH, '//*[@id="job_container"]/div[7]/table/tbody/tr[2]/td').text

        data = {
            'title': detail_link_connect[0],
            'url': detail_link_connect[1],
            'workplace': workplace,
            'recruitment_staff': recruitment_staff + "/" + gender + "/" + age,
            'recruitment_field': recruitment_field,
            'qualification_license': qualification_license,
            'job_specifications': job_specifications,
            'employment': employment,
            'wages': wages,
            'business_hours': business_hours,
            'recruiter': recruiter,
            'contact_address': contact_address
        }

        announcement_list_Busan_Busan.append(data)

        sheet.append([detail_link_connect[0], detail_link_connect[1], workplace,
                      recruitment_staff + "/" + gender + "/" + age, recruitment_field,
                      qualification_license, job_specifications, employment,
                      wages, business_hours, recruiter, contact_address])

    return announcement_list_Busan_Busan


def pass_the_next_link(driver):
    next_link = driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'li')

    return next_link


def main(driver):
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'https://www.busan50plus.or.kr/job/civilian_02_2'

    # 웹드라이버 열기
    # options=options 추가해주기
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(3)

    # 시트 만들기
    xlsx.create_sheet("부산포털")
    sheet = xlsx["부산포털"]
    sheet.append(['제목', 'URL', '근무지', '모집인원', '모집분야', '우대사항',
                  '내용', '고용형태', '급여액', '근무시간', '채용담당자',
                  '연락처'])

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Busan_Busan = []

    next_link = pass_the_next_link(driver)
    detail_link = list()
    for i in range(len(next_link)):
        try:
            detail_link.append(next_link[i].find_element(By.TAG_NAME, 'a').get_attribute('href'))
        except NoSuchElementException:
            pass

    index = 0
    while index < len(detail_link):
        notices = approach_the_list(driver)
        detail_link_list = extract_url(notices)
        announcement_list_Busan_Busan = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list,
                                                                                          sheet,
                                                                                          announcement_list_Busan_Busan)
        driver.get(detail_link[index])
        index = index + 1

    del xlsx['Sheet']  # 기본 시트 삭제
    filename = "C:/Python/" + "부산포털" + "_NewList.xlsx"
    xlsx.save(filename)  # 통합문서 저장
    xlsx.close()  # 통합문서 종료

    # driver.close()
    # driver.quit()

    return announcement_list_Busan_Busan