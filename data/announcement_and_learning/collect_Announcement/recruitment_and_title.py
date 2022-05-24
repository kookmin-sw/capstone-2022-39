import logging
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


def detail_collect_Announcement(url, sheet, data_list):
    count = 0
    for data in data_list:
        # print(data)
        params = {
            'authKey': '',
            'callTp': 'D',
            'returnType': 'XML',
            'wantedAuthNo': data,
            'infoSvc': 'VALIDATION'
        }
        # Ordered dictionary type
        try:
            response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
            time.sleep(1)

            result = xmltodict.parse(response.text)
        except ExpatError:
            pass
        except Exception as e:
            print(f"Exception occured:\n{e}")
            time.sleep(1)
            response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
            result = xmltodict.parse(response.text)

        # dictionlay type
        dd = json.loads(json.dumps(result))
        # print(dd)
        # print(type(dd))

        body = dd['wantedDtl']
        # print(body)

        # Dataframe으로 만들기
        dataframe = pd.json_normalize(body)
        # data_detail_list = dataframe['wantedRoot']['wanted']
        try:
            # 제목
            title = '{0}'.format(dataframe['wantedInfo.wantedTitle'].values[0])

            # 모집 분야 추출
            regex = "\(.*\)|\s-\s.*"
            text = '{0}'.format(dataframe['wantedInfo.jobsNm'].values[0])
            recruitment_field = re.sub(regex, '', text)
            print(recruitment_field)

            sheet.append([title, recruitment_field])
            print(count)
            count = count + 1
        except KeyError:
            print("error: " + data)
            count = count + 1
            pass
        except ConnectionError:
            logging.error('Data of %s not retrieved because \nURL: %s', recruitment_field, url)
        except TimeoutError:
            logging.error("타임아웃 발생 - URL %s", url)
        else:
            logging.error("성공")


def main():
    # 고정 URL
    url = 'http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?'

    # 시트 만들기
    xlsx.create_sheet("워크넷모집분야")
    sheet = xlsx["워크넷모집분야"]
    sheet.append(['제목', '모집분야'])

    data_list = pd.read_excel('C:/Python/공고수집/공고(URL)/워크넷(공고-1).csv')

    detail_collect_Announcement(url, sheet, data_list['모집분야'])

    del xlsx['Sheet']  # 기본 시트 삭제
    filename = "C:/Python/" + "워크넷(모집분야-1)" + "_NewList.xlsx"
    xlsx.save(filename)  # 통합문서 저장
    xlsx.close()  # 통합문서 종료


main()
