import pprint
from pyexpat import ExpatError

import requests
import json
import xmltodict
import time
import re
import pandas as pd
from openpyxl import Workbook

# 통합문서 열기

xlsx = Workbook()


def collect_Announcement(url):
    data_list = list()
    for i in range(1, 500):
        params = {
            'authKey': '',
            'callTp': 'L',
            'returnType': 'XML',
            'startPage': i,
            'display': '100',
            'pfPreferential': 'S'
        }

        response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
        time.sleep(5)

        if response.status_code == 200:
            # Ordered dictionary type
            result = xmltodict.parse(response.text)

            # dictionlay type
            dd = json.loads(json.dumps(result))

            try:
                body = dd['wantedRoot']['wanted']

                # Dataframe으로 만들기
                dataframe = pd.json_normalize(body)
                # print(dataframe)
                # print(dataframe['wantedAuthNo'])
                data_detail_list = dataframe['wantedAuthNo']

                for data in data_detail_list:
                    data_list.append(data)
                    print(data)

            except KeyError:
                print("error: " + data)
                break

    return data_list


def detail_collect_Announcement(url, sheet, data_list):
    for data in data_list:
        params = {
            'authKey': '',
            'callTp': 'D',
            'returnType': 'XML',
            'wantedAuthNo': data,
            'infoSvc': 'VALIDATION'
        }
        print(data)
        response = requests.get(url, params=params, headers={'User-Agent':'Mozilla/5.0'})
        time.sleep(3)

        if response.status_code == 200:
            # Ordered dictionary type
            try:
                result = xmltodict.parse(response.text)
            except ExpatError:
                break

            # dictionlay type
            dd = json.loads(json.dumps(result))
            # print(dd)
            # print(type(dd))

            body = dd['wantedDtl']
            # print(body)

            # Dataframe으로 만들기
            dataframe = pd.json_normalize(body)
            # print(dataframe)
            # data_detail_list = dataframe['wantedRoot']['wanted']
            try:
                # 구인제목
                title = '{0}'.format(dataframe['wantedInfo.wantedTitle'].values[0])

                # URL 추출
                URL = '{0}'.format(dataframe['wantedInfo.dtlRecrContUrl'].values[0])

                # 근무지 추출
                workplace = '{0}'.format(dataframe['wantedInfo.workRegion'].values[0])

                # 모집 인원 추출
                recruitment_staff = '{0}'.format(dataframe['wantedInfo.collectPsncnt'].values[0])

                # 모집 분야 추출
                regex = "\(.*\)|\s-\s.*"
                text = '{0}'.format(dataframe['wantedInfo.jobsNm'].values[0])
                recruitment_field = re.sub(regex, '', text)

                # 우대 사항 추출
                qualification_license = '{0}'.format(dataframe['wantedInfo.pfCond'].values[0])

                # 내용 추출
                job_specifications = '{0}'.format(dataframe['wantedInfo.jobCont'].values[0])

                # 고용 형태 추출
                employment = '{0}'.format(dataframe['wantedInfo.empTpNm'].values[0])

                # 급여액 추출
                wages = '{0}'.format(dataframe['wantedInfo.salTpNm'].values[0])

                # 근무 시간 추출
                business_hours = '{0}'.format(dataframe['wantedInfo.workdayWorkhrCont'].values[0])

                # 채용 담당자 추출
                recruiter = '{0}'.format(dataframe['wantedInfo.rcptMthd'].values[0])

                # 연락처 추출
                try:
                    contact_address = '{0}'.format(dataframe['empchargeInfo.contactTelno'].values[0])
                except KeyError:
                    contact_address = " "

                sheet.append([title, URL, workplace,
                              recruitment_staff, recruitment_field,
                              qualification_license, job_specifications, employment,
                              wages, business_hours, recruiter, contact_address])
            except KeyError:
                print("error: " + data)
                pass


def main():
    # 고정 URL
    url = 'http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?'

    # 시트 만들기
    xlsx.create_sheet("워크넷")
    sheet = xlsx["워크넷"]
    sheet.append(['제목', 'URL', '근무지', '모집인원', '모집분야', '우대사항',
                  '내용', '고용형태', '급여액', '근무시간', '채용담당자',
                  '연락처'])

    data_list = collect_Announcement(url)
    detail_collect_Announcement(url, sheet, data_list)

    del xlsx['Sheet']  # 기본 시트 삭제
    filename = "C:/Python/" + "워크넷" + "_NewList.xlsx"
    xlsx.save(filename)  # 통합문서 저장
    xlsx.close()  # 통합문서 종료


main()
