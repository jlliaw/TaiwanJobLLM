# 生成式AI及檢索式增強生成在政府開放資料的整合應用-勞動力發展署台灣就業通

## 本範例使用台灣就業通開放資料做為擴增知識庫並整合繁體中文大語言模型 TAIDE 以及建立求職問答機制。
1. 台灣就業通開放資料: https://data.gov.tw/dataset/44062
   官方提供的資料欄位較多(19個)而且是英文，只留下求職時可能會使用的條件(10個欄位)做為擴增知識庫的資料並轉成中文。相關程式如 getDataFromDataGov.py :
```
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

```

最後產生的資料如 getDataFromDataGov.json 格式, 因為本範例考量執行平台硬體效能, 僅使用150筆求才資料做為知識庫。

2. TAIDE 大語言模型 : https://huggingface.co/taide/Llama3-TAIDE-LX-8B-Chat-Alpha1
繁體中文模型，參數量為8B, 相對容易落地, 因為使用此一模型做為生成式AI模型。

3. 部署完成後結果 :
![image](https://github.com/jlliaw/TaiwanJobLLM/blob/main/ref/demonstrator.gif)

reference : https://blog.darkthread.net/blog/rag/
