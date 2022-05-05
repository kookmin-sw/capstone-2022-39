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
    # time.sleep(2)
    notices = driver.find_element(By.CLASS_NAME, 'scroll-no.m_guin.scroll-no') \
        .find_element(By.TAG_NAME, 'tbody') \
        .find_elements(By.TAG_NAME, 'tr')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(steady_number, index):
    title_name_and_detail_link_list = list()  # 제목 및 상세 페이지를 위한 URL 수집

    time.sleep(3)
    index_url = (index - 2) * 15
    for i in range(0, 15):
        try:
            steady_url = "https://changwon6588.or.kr/incruit/guinSituation_view.php?idx="

            detail_link = steady_url + str(steady_number - index_url + 2810)

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
        section = driver.find_element(By.XPATH,
                                      '/html/body/div/article/div[2]/div[2]/div[2]/section/div/div/div['
                                      '1]/div/div/div[1]/span').text

        if section == "모집중":

            detail_title = driver.find_element(By.XPATH, '/html/body/div/article/div[2]/div[2]/div['
                                                         '2]/section/div/div/div[1]/div/div/div[1]/strong').text

            time.sleep(2)

            other = driver.find_element(By.XPATH, '/html/body/div/article/div[2]/div[2]/div[2]/section/div/div/div['
                                                  '3]/div[2]/table/tbody/tr[10]/td').text

            split_list = other.split('\n')

            job_specifications = ''
            business_hours = ''
            qualification_license = ''

            for i in range(len(split_list)):
                if split_list[i].__contains__("내용") or split_list[i].__contains__("대상"):
                    # 내용 추출
                    job_specifications = split_list[i]
                elif split_list[i].__contains__("시간") or split_list[i].__contains__("근무시간"):
                    # 근무 시간 추출
                    business_hours = split_list[i]
                elif split_list[i].__contains__("*") or split_list[i].__contains__("※"):
                    # 우대 사항 추출
                    qualification_license = qualification_license + split_list[i]
                else:
                    pass

            # 근무지 추출
            workplace = driver.find_element(By.XPATH, '/html/body/div/article/div[2]/div[2]/div[2]/section/div/div/div['
                                                      '3]/div[2]/table/tbody/tr[1]/td').text

            # 모집 인원 추출
            recruitment_staff = driver.find_element(By.XPATH,
                                                    '/html/body/div/article/div[2]/div[2]/div[2]/section/div/div/div['
                                                    '3]/div[ '
                                                    '2]/table/tbody/tr[8]/td').text

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

            # 성별 추출
            gender = driver.find_element(By.XPATH, '/html/body/div/article/div[2]/div[2]/div[2]/section/div/div/div['
                                                   '3]/div[ '
                                                   '2]/table/tbody/tr[6]/td').text

            # 연령 추출
            age = driver.find_element(By.XPATH,
                                      '/html/body/div/article/div[2]/div[2]/div[2]/section/div/div/div[3]/div['
                                      '2]/table/tbody/tr[5]/td').text

            # 고용 형태 추출
            employment = driver.find_element(By.XPATH, '/html/body/div/article/div[2]/div[2]/div['
                                                       '2]/section/div/div/div[ '
                                                       '3]/div[2]/table/tbody/tr[7]/td').text

            # 급여액 추출
            wages = driver.find_element(By.XPATH,
                                        '/html/body/div/article/div[2]/div[2]/div[2]/section/div/div/div[3]/div['
                                        '2]/table/tbody/tr[9]/td').text

            # 채용 담당자 추출
            recruiter = "창원노인일자리창출지원센터 "

            # 연락처 추출
            contact_address = "전화문의 055)286-6588"

            detail_page_text.append(
                [detail_title, detail_link_connect[0], workplace,  recruitment_staff + "/" + gender + "/" + age,
                 recruitment_field, qualification_license, job_specifications, employment,
                 wages, business_hours, recruiter, contact_address])

    return detail_page_text


def pass_the_next_link(driver):
    links = driver.find_element(By.CLASS_NAME, 'paginate').find_elements(By.TAG_NAME, 'a')

    return links


def main():
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'https://changwon6588.or.kr/incruit/guinSituation.php?s_sex=&s_name=&s_age_s=&s_age_e=&s_job_type=&page=1'

    # 웹드라이버 열기
    # options=options 추가해주기
    driver = webdriver.Chrome('C:/chromedriver.exe')
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(3)

    # 시트 만들기
    xlsx.create_sheet("창원노인일자리창출지원센터")
    sheet = xlsx["창원노인일자리창출지원센터"]
    sheet.append(['제목', 'URL', '근무지', '모집인원', '모집분야', '우대사항',
                  '내용', '고용형태', '급여액', '근무시간', '채용담당자',
                  '연락처'])

    next_link = pass_the_next_link(driver)
    detail_link = list()
    for i in range(len(next_link)):
        detail_link.append(next_link[i].get_attribute('href'))

    steady_number = driver.find_element(By.XPATH, '/html/body/div/article/div[2]/div[2]/div[2]/section/div/div/div['
                                                  '2]/div/table/tbody/tr[1]/td[1]/span').text
    index = 2
    while index < len(next_link) - 2:
        detail_link_list = extract_url(int(steady_number), index)
        detail_page_text = approach_detail_link_and_extract_recruitment_info(driver, detail_link_list)
        for link_list, page_text in zip(detail_link_list, detail_page_text):
            sheet.append(page_text)

        driver.get(detail_link[index])
        index = index + 1
        time.sleep(2)

    del xlsx['Sheet']  # 기본 시트 삭제
    filename = "C:/Python/" + "창원노인일자리창출지원센터" + "_NewList.xlsx"
    xlsx.save(filename)  # 통합문서 저장
    xlsx.close()  # 통합문서 종료

    driver.close()
    driver.quit()


main()
