"""
- selenium Ver : 3.14.1
- 포항노인일자리창출지원센터
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import time
from openpyxl import Workbook

# 통합문서 열기
xlsx = Workbook()


# 공고 내용을 상세히 파악하기 위해 element를 이용해 리스트에 접근
def approach_the_list(driver):
    # time.sleep(2)
    notices = driver.find_element(By.CLASS_NAME, 'st_mybd_list') \
        .find_element(By.TAG_NAME, 'tbody') \
        .find_elements(By.TAG_NAME, 'tr')

    return notices


# 리스트에서 상세 페이지로 갈 수 있는 URL 추출
def extract_url(notices):
    title_name_and_detail_link_list = list()  # 제목 및 상세 페이지를 위한 URL 수집

    for notice in notices:
        try:
            seperate_section = notice.find_elements(By.TAG_NAME, 'td')
            section = seperate_section[6].text
            # print(section)

            if section == "구인진행":
                detail_title = notice.find_element(By.CLASS_NAME, 'st_mybd_subject.st_mybd_m_show_td').text
                detail_link = "http://m.phsjc1919.or.kr/shop_contents/myboard_form.htm?load_type=&myboard_code" \
                              "=st_myboard "

                # 근무지 추출
                workplace = '-'

                # 모집 인원 추출
                recruitment_staff = '-'

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
                job_specifications = '-'

                # 고용 형태 추출
                employment = seperate_section[3].text

                # 급여액 추출
                wages = seperate_section[2].text

                # 근무 시간 추출
                business_hours = '-'

                # 연령 추출
                age = seperate_section[4].text

                # 채용담당자 추출
                recruiter = "포항노인일자리창출지원센터"

                # 연락처 추출
                contact_address = "고객센터: 054-231-1919"

                title_name_and_detail_link_list.append([detail_title, detail_link, workplace, recruitment_staff + age,
                                                         recruitment_field, qualification_license, job_specifications, employment,
                                                         wages, business_hours, recruiter, contact_address])
        except NoSuchElementException:
            pass

    return title_name_and_detail_link_list


def pass_the_next_link(driver):
    links = driver.find_element(By.CLASS_NAME, 'ui-pagenate').find_elements(By.TAG_NAME, 'a')

    return links


def main():
    # 윈도우 사이즈
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    url = 'http://m.phsjc1919.or.kr/shop_contents/myboard_list.htm?page=1&myboard_code=st_myboard'

    # 웹드라이버 열기
    # options=options 추가해주기
    driver = webdriver.Chrome('C:/chromedriver.exe')
    driver.get(url)

    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    time.sleep(5)

    # 시트 만들기
    xlsx.create_sheet("포항노인일자리창출지원센터")
    sheet = xlsx["포항노인일자리창출지원센터"]
    sheet.append(['제목', 'URL', '근무지', '모집인원', '모집분야', '우대사항',
                  '내용', '고용형태', '급여액', '근무시간', '채용담당자',
                  '연락처'])

    next_link = pass_the_next_link(driver)

    index = 0
    while index < len(next_link) - 2:
        notices = approach_the_list(driver)
        detail_link_list = extract_url(notices)

        for page_text in detail_link_list:
            sheet.append(page_text)

        fix_url = "http://m.phsjc1919.or.kr/shop_contents/myboard_list.htm?page="
        fix_sub_url = "&myboard_code=st_myboard"
        driver.get(fix_url + str(index+2) + fix_sub_url)
        index = index + 1
        time.sleep(3)

    del xlsx['Sheet']  # 기본 시트 삭제
    filename = "C:/Python/" + "포항노인일자리창출지원센터" + "_NewList.xlsx"
    xlsx.save(filename)  # 통합문서 저장
    xlsx.close()  # 통합문서 종료

    driver.close()
    driver.quit()


main()
