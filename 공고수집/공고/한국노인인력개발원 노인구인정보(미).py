import pprint
import requests
import json
import xmltodict
import time

import pandas as pd

url = 'http://apis.data.go.kr/B552474/SenuriService/getJobList'

for i in range(1, 2):
    data_list = list()
    params = {'serviceKey': '',
              'numOfRows': '100',
              'pageNo': i
              }

    response = requests.get(url, params=params)
    time.sleep(5)

    if response.status_code == 200:
        # Ordered dictionary type
        result = xmltodict.parse(response.text)

        # dictionlay type
        dd = json.loads(json.dumps(result))
        try:

            body = dd['response']['body']['items']
            # print(body)

            # 데이터 결과값 예쁘게 출력해주는 코드
            pp = pprint.PrettyPrinter(indent=4)
            # print(pp.pprint(body))

            # Dataframe으로 만들기
            dataframe = pd.json_normalize(body['item'])
            data_job_list = dataframe['jobId']
            # print(data_job_list)

            for data in data_job_list:
                data_list.append(data)
                print(data)

        except KeyError:
            print("Error")
            break


# 이모티콘(emoji) 삭제/제거
def rmEmoji(inputData):
    return inputData.encode('utf-8', 'ignore').decode('utf-8')