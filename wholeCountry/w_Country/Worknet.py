"""
- 워크넷
"""
from pyexpat import ExpatError
import requests
import json
import xmltodict
import pandas as pd
import time
import re
from datetime import datetime
from wholeCountry.areas_of_recruitment import areas_of_recruitment


def collect_Announcement(url):
    data_list = list()
    for i in range(1, 300):
        params = {
            'authKey': 'WNL2I9NGDJD367EORE44Y2VR1HJ',
            'callTp': 'L',
            'returnType': 'XML',
            'startPage': i,
            'display': '100',
            'pfPreferential': 'S'
        }
        time.sleep(2)
        try:
            response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})

            # Ordered dictionary type
            result = xmltodict.parse(response.text)

            # dictionlay type
            dd = json.loads(json.dumps(result))

            body = dd['wantedRoot']['wanted']

            # Dataframe으로 만들기
            dataframe = pd.json_normalize(body)

            data_detail_list = dataframe['wantedAuthNo']

            for data in data_detail_list:
                data_list.append(data)
                # print(data)

        except KeyError:
            # print("error: " + data)
            break
        except ConnectionError:
            pass
        except TimeoutError:
            pass

    return data_list


def detail_collect_Announcement(url, data_list, announcement_list_Worknet):
    index = 0
    for data in data_list:
        params = {
            'authKey': 'WNL2I9NGDJD367EORE44Y2VR1HJ',
            'callTp': 'D',
            'returnType': 'XML',
            'wantedAuthNo': data,
            'infoSvc': 'VALIDATION'
        }
        # print(data)

        try:
            response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
            # time.sleep(1)

            # Ordered dictionary type
            try:
                result = xmltodict.parse(response.text)
            except ExpatError:
                pass

            # dictionlay type
            dd = json.loads(json.dumps(result))

            body = dd['wantedDtl']

            # Dataframe으로 만들기
            dataframe = pd.json_normalize(body)

            # 구인제목
            title = '{0}'.format(dataframe['wantedInfo.wantedTitle'].values[0])
            # print(title)

            # URL 추출
            URL = '{0}'.format(dataframe['wantedInfo.dtlRecrContUrl'].values[0])

            # 근무지 추출
            workplace = '{0}'.format(dataframe['wantedInfo.workRegion'].values[0])

            # 모집 인원 추출
            recruitment_staff = '{0}'.format(dataframe['wantedInfo.collectPsncnt'].values[0]) + "명"

            # 모집 분야 추출
            # regex = "\(.*\)|\s-\s.*"
            # text = '{0}'.format(title)
            recruitment_field = areas_of_recruitment(title)

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
            recruiter = '워크넷'
            # recruiter = '{0}'.format(dataframe['wantedInfo.rcptMthd'].values[0])

            # 등록일
            registration_date = "-"

            # primary key
            modify_title = re.sub('[^A-Za-z0-9가-힣]', '', title)
            modify_recruiter = re.sub('[^A-Za-z0-9가-힣]', '', recruiter)
            modify_workplace = re.sub('[^A-Za-z0-9가-힣]', '', workplace)
            primary_key = "W" + str(modify_title) + "#" + str(modify_recruiter) + "#" + str(modify_workplace)

            index = index + 1

            # 연락처 추출
            try:
                contact_address = '{0}'.format(dataframe['empchargeInfo.contactTelno'].values[0])

                if contact_address == "None":
                    contact_address = "-"
            except KeyError:
                contact_address = "-"

            data = {
                'title': title,
                'url': URL,
                'workplace': workplace,
                'recruitment_staff': recruitment_staff,
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

            announcement_list_Worknet.append(data)

        except KeyError:
            pass
        except ConnectionError:
            pass
        except TimeoutError:
            pass

    return announcement_list_Worknet


def main():
    # 고정 URL
    url = 'http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?'

    # dict type의 공고를 담기 위한 리스트 선언
    announcement_list_Worknet = []

    data_list = collect_Announcement(url)
    announcement_list_Worknet = detail_collect_Announcement(url, data_list, announcement_list_Worknet)

    return announcement_list_Worknet


