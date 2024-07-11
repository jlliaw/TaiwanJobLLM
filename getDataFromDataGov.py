import requests
import json

# Get data from data.gov.sg
def getDataFromDataGov(url):
    
    response = requests.get(url)
    data = response.json()
    return data 

limit = 100
offset = 100
offsetidx = 0

taichungjob = []

while len(taichungjob) <= 150:

    offsetpara = offsetidx * offset
    url = f"https://apiservice.mol.gov.tw/OdService/rest/datastore/A17000000J-030144-nkP?limit={limit}&offset={offsetpara}"

    data = getDataFromDataGov(url)

    for d in data['result']['records']:    
        if '北市' in d['CITYNAME']:
            tchjob = {}
            tchjob['職缺'] = d['OCCU_DESC']
            tchjob['職缺類別'] = d['WK_TYPE']
            tchjob['職缺說明'] = d['JOB_DETAIL']
            tchjob['工作地點'] = d['CITYNAME']
            tchjob['工作經驗'] = d['EXPERIENCE']
            tchjob['工作時段'] = d['WKTIME']
            tchjob['敘薪方式'] = d['SALARYCD']
            tchjob['薪資'] = d['NT_L']
            tchjob['學歷'] = d['EDGRDESC']
            tchjob['公司名稱'] = d['COMPNAME']

            taichungjob.append(tchjob)

    offsetidx += 1

print(taichungjob)
# Convert and write JSON object to file
with open("getDataFromDataGov.json", "w", encoding='utf8') as outfile: 
    json.dump(taichungjob, outfile, indent = 2, sort_keys = True, ensure_ascii=False)

pass