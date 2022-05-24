# selenium Ver : 3.14.1
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from wholeCountry.areas_of_recruitment import areas_of_recruitment
import re


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    notices = driver.find_element(By.CLASS_NAME, 'job.tbl.margin-t10.cle') \
        .find_element(By.TAG_NAME, 'tbody') \
        .find_elements(By.TAG_NAME, 'tr')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices):
    title_name_and_detail_link_list = list()  # 제목 및 상세 페이지를 위한 URL 수집

    for notice in notices:
        try:
            section = notice.find_element(By.CLASS_NAME, 'status.recurit-open').text
            if section == "모집중":
                detail_title = notice.find_element(By.CLASS_NAME, 'cls_ellipsis_subjct').text
                detail_link = notice.find_element(By.CLASS_NAME, 'cls_ellipsis_subjct') \
                    .get_attribute('href')
                registration_date = notice.find_elements(By.TAG_NAME, 'td')[5].text
                registration_date = registration_date.replace('.', '/')

                title_name_and_detail_link_list.append([detail_title, detail_link, registration_date[2:10]])
        except NoSuchElementException:
            pass

    return title_name_and_detail_link_list


def approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Gyeongnam_Jinju):
    for detail_link_connect in detail_link_list:
        # 추출된 URL(상세 페이지) 이동
        driver.get(str(detail_link_connect[1]))

        # 근무지 추출
        workplace = driver.find_element(By.XPATH, '//*[@id="mm-0"]/div[1]/div[5]/div[2]/table/tbody/tr[1]/td[1]').text

        # 모집 인원 추출
        recruitment_staff = driver.find_element(By.XPATH,
                                                '//*[@id="mm-0"]/div[1]/div[5]/div[2]/table/tbody/tr[2]/td[1]').text

        # 성별 추출
        gender = driver.find_element(By.XPATH, '//*[@id="mm-0"]/div[1]/div[5]/div[2]/table/tbody/tr[3]/td[1]').text

        # 연령 추출
        age = driver.find_element(By.XPATH, '//*[@id="mm-0"]/div[1]/div[5]/div[2]/table/tbody/tr[3]/td[2]').text

        # 우대사항 추출
        qualification_license = driver.find_element(By.XPATH,
                                                    '//*[@id="mm-0"]/div[1]/div[5]/div[2]/table/tbody/tr[4]/td[2]').text

        # 내용 추출
        job_specifications = driver.find_element(By.XPATH,
                                                 '//*[@id="mm-0"]/div[1]/div[5]/div[2]/table/tbody/tr[5]/td').text

        # 고용형태 추출
        employment = '-'

        # 급여액 추출
        wages = driver.find_element(By.XPATH,
                                    '//*[@id="mm-0"]/div[1]/div[5]/div[2]/table/tbody/tr[1]/td[2]').text

        # 근무 시간 추출
        business_hours = driver.find_element(By.XPATH,
                                             '//*[@id="mm-0"]/div[1]/div[5]/div[2]/table/tbody/tr[4]/td[1]').text

        # 채용 담당자 추출
        recruiter = "진주노인일자리창출지원센터 "

        # 연락처 추출
        contact_address = "전화문의) 055-744-6088, 055-758-5060"

        # 등록일
        registration_date = detail_link_connect[2]

        # 모집 분야
        recruitment_field = areas_of_recruitment(detail_link_connect[0] + job_specifications)

        # primary key
        modify_title = re.sub('[^A-Za-z0-9가-힣]', '', detail_link_connect[0])
        modify_recruiter = re.sub('[^A-Za-z0-9가-힣]', '', recruiter)
        modify_workplace = re.sub('[^A-Za-z0-9가-힣]', '', workplace)
        primary_key = "J" + str(modify_title) + "#" + str(modify_recruiter) + "#" + str(modify_workplace)

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
            'contact_address': contact_address,
            'registration_date': registration_date,
            'primary_key': primary_key
        }

        announcement_list_Gyeongnam_Jinju.append(data)

    return announcement_list_Gyeongnam_Jinju


def pass_the_next_link(driver):
    links = driver.find_element(By.CLASS_NAME, 'paging').find_elements(By.CLASS_NAME, 'pjax')

    return links


def main(driver):
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'http://jej.or.kr/%EA%B5%AC%EC%9D%B8%EA%B5%AC%EC%A7%81/%EA%B5%AC%EC%9D%B8%EC%A0%95%EB%B3%B4/?pg=1'

    # 웹드라이버 열기
    # options=options 추가해주기
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(5)

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Gyeongnam_Jinju = []

    next_link = pass_the_next_link(driver)
    detail_link = list()
    for i in range(len(next_link)):
        detail_link.append(next_link[i].get_attribute('href'))

    index = 0
    while index < len(next_link) - 1:
        notices = approach_the_list(driver)
        detail_link_list = extract_url(notices)
        announcement_list_Gyeongnam_Jinju = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list, announcement_list_Gyeongnam_Jinju)

        driver.get(detail_link[index])
        index = index + 1
        time.sleep(1)

    return announcement_list_Gyeongnam_Jinju
