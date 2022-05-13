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


def collect_Announcement(url, sheet):
    data_list = list()
    for i in range(1, 400):
        params = {
            'authKey': '',
            'callTp': 'L',
            'returnType': 'XML',
            'startPage': i,
            'display': '10',
            'untilEmpWantedYn': 'Y',
            'pfPreferential': 'S'

        }

        try:
            response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
            time.sleep(1)

            # Ordered dictionary type
            result = xmltodict.parse(response.text)

            # dictionlay type
            dd = json.loads(json.dumps(result))

            body = dd['wantedRoot']['wanted']

            # Dataframe으로 만들기
            dataframe = pd.json_normalize(body)
            # print(dataframe)
            # print(dataframe['wantedAuthNo'])
            data_detail_list = dataframe['wantedAuthNo']

            for data in data_detail_list:
                data_list.append(data)
                # print(data)
                sheet.append([data])

        except KeyError:
            print("error: " + data)
            break
        except ConnectionError:
            pass
        except TimeoutError:
            pass

    return data_list


def main():
    # 고정 URL
    url = 'http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?'

    # 시트 만들기
    xlsx.create_sheet("워크넷모집분야")
    sheet = xlsx["워크넷모집분야"]
    sheet.append(['모집분야'])

    data_list = collect_Announcement(url, sheet)

    del xlsx['Sheet']  # 기본 시트 삭제
    filename = "C:/Python/" + "워크넷(공고)" + "_NewList.xlsx"
    xlsx.save(filename)  # 통합문서 저장
    xlsx.close()  # 통합문서 종료


main()
