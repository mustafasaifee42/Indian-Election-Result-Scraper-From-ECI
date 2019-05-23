from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


with open('data_combined.json', "r") as read_file:
    dataList = json.load(read_file)

UPA=['INC','DMK','RJD','JD(S)','BLSP','JMM','CPM','HAM','VIP','CPI','IUML','JAP','VCK','JVM','SWP','BVA','YSP','CPI(ML)(L)','KEC(M)','RSP','KMDK','IJK','MDMK','JKN']
NDA=['BJP','SHS','ADMK','JD(U)','SAD','PMK','LJP','DMDK','BDJS','AGP','AD','AJSU','PT','PNK','AINRC','BOPF','NDPP','RSP']
Mahagatbandhan=['BSP','SP']


urlList =[]
for data in dataList:
    url = 'https://results.eci.gov.in/pc/en/constituencywise/Constituencywise'+ data['stateCode']+ data['Constituency No'] +'.htm?ac='+ data['Constituency No']
    url1 = url
    html = urlopen(url1)

    soup = BeautifulSoup(html,'html.parser')

    tab=soup.findAll("table",{"class":"table-party"})

    tr = tab[0].findAll('tr')

    arr = []
    for i in range (3,len(tr)-1):
        tds = tr[i].findAll('td')
        arr.append([])
        for td in tds:
            arr[len(arr)-1].append(td.text)
        arr[len(arr)-1][len(arr[len(arr)-1])-2] = int(arr[len(arr)-1][len(arr[len(arr)-1])-2])
    sorted_list = sorted(arr, key=lambda x: x[len(arr[0])-2],reverse=True)
    if data['Name']=='Vellore':
        data['2019-Result']={
          "1":{
            "Name": "NA",
            "Party": "NA",
            "Alliance":"Others",
            "Votes": 1
          },
          "2":{
            "Name": "NA",
            "Party": "NA",
            "Alliance":"Others",
            "Votes": 1
          },
          "VotersInfo": {
            "TurnOut": "NA",
            "TotalVoters": "NA",
            "TurnOutPercentage": "NA"
          }
        }
    else:
        data['2019-Result']={}
        for k in range(0,len(sorted_list)):
            data['2019-Result'][str(k+1)]={}
            data['2019-Result'][str(k+1)]['Name']=sorted_list[k][1]
            data['2019-Result'][str(k+1)]['Party']=sorted_list[k][2]
            data['2019-Result'][str(k + 1)]["Alliance"] = "Others"
            if sorted_list[k][2] in UPA:
                data['2019-Result'][str(k + 1)]["Alliance"] = "UPA"
            if sorted_list[k][2] in NDA:
                data['2019-Result'][str(k + 1)]["Alliance"] = "NDA"
            if sorted_list[k][2] in Mahagatbandhan:
                data['2019-Result'][str(k + 1)]["Alliance"] = "Mahagatbandhan"
            data['2019-Result'][str(k+1)]['Votes']=sorted_list[k][len(sorted_list[0])-2]
            data['2019-Result']['VotersInfo']={}
            data['2019-Result']['VotersInfo']['TurnOut'] = 'NA'
            data['2019-Result']['VotersInfo']['TotalVoters'] = 'NA'
            data['2019-Result']['VotersInfo']['TurnOutPercentage'] = 'NA'


with open("data_scraped_9_22.json", "w") as write_file:
    json.dump(dataList, write_file, indent=2)

with open("data_scraped.json", "w") as write_file:
    json.dump(dataList, write_file, indent=2)