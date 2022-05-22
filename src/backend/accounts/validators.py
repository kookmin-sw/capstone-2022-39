import requests
import json
from django.core.exceptions import ValidationError


def company_id_validator(value):
    SERVICE_KEY = "fBsTHfPJGwtfAXV8AUEs%2BbePcFnlBWXOUFL43JGpOK%2ByY4eLmfeLAF2O7MBgVp9ggJCVTDXB9JwCmJv7I8XfOg%3D%3D"
    url = f"https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey={SERVICE_KEY}&returnType=JSON"

    company_no = value.replace('-', '')
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

def validate_company_id(value):
    if company_id_validator(value) is True:
        return value
    else:
        raise ValidationError("잘못된 사업자 등록번호 입니다.")