import requests
import json
import boto3


def get_keys():
    with open("keys.json", "r") as open_keys:
        keys = json.load(open_keys)

    return keys['sgis']


def sgis_auth(event, context):
    keys = get_keys()
    consumer_key = keys["CONSUMER_KEY"]
    consumer_secret = keys["CONSUMER_SECRET"]

    auth_url = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"

    param = {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret
    }

    res = requests.get(auth_url, params=param)
    res_to_dict = json.loads(res.text)
    access_token = res_to_dict['result']['accessToken']

    return sgis_get_address(access_token)


def sgis_get_info_api(token: str, cd=None):

    api_url = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json"

    param = {
        "accessToken": token
    }

    if cd:
        param["cd"] = cd

    res = requests.get(api_url, params=param)
    res_to_dict = json.loads(res.text)
    return res_to_dict['result']


def sgis_get_address(token: str):
    # lev1: 시/도
    # lev2: 구/군/시
    # lev3: 동/읍/면

    lev1_res = sgis_get_info_api(token)
    addr_dict = dict()

    for elem in lev1_res:
        addr_dict[elem.get('addr_name')] = elem.get('cd')

    for key, val in addr_dict.items():
        lev2_res = sgis_get_info_api(token, cd=val)
        lev2_dict = dict()

        for elem in lev2_res:
            lev3_list = list()
            addr_name = elem.get('addr_name')
            cd = elem.get('cd')

            lev3_res = sgis_get_info_api(token, cd=cd)

            for lev3_elem in lev3_res:
                lev3_list.append(lev3_elem['addr_name'])

            lev2_dict[addr_name] = lev3_list

        addr_dict[key] = lev2_dict

    with open('/tmp/address.json', 'w', encoding="UTF-8") as f:
        json.dump(addr_dict, f, indent=4, ensure_ascii=False)

    save_to_s3()


def save_to_s3():
    s3 = boto3.client('s3')
    bucket_name = "addr-info"
    file_name = "address.json"

    s3.upload_file(f"/tmp/{file_name}", bucket_name, file_name)
