import requests
import json


def get_keys():
    with open("keys.json", "r") as open_keys:
        keys = json.load(open_keys)

    return keys['odcloud']

def validator(value):
    keys = get_keys()
    SERVICE_KEY = keys["SERVICE_KEY"]
    url = f"https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey={SERVICE_KEY}&returnType=JSON"

    company_no = "3128105829"

    headers = {
        "Content-Type": "application/json"
    }

    json_body = {
        "b_no": [
            company_no
        ]
    }

    res = requests.post(url, headers=headers, data=json.dumps(json_body))
    dic_res = json.loads(res.text)
    get_status = dic_res['data'][0]['b_stt']

    if '계속사업자' in get_status:
        return True
    else:
        return False
