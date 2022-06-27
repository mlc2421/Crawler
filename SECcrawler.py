import requests
import pandas as pd
import numpy as np
import time
import random
from bs4 import BeautifulSoup

Final_Dataframe=pd.DataFrame(columns=["Company","report link","Result"])


def SEC(company,date,keyword):

    endpoint="https://www.sec.gov/cgi-bin/browse-edgar"

    param_dict={"action":"getcompany",
                "CIK":str(company),
                "type":"10-k",
                "dateb":str(date),
                "owner":"exclude",
                "start":"",
                "output":"",
                "count":'100'}

    respo=requests.get(url=endpoint,params=param_dict)
    urlc=respo.url


    #搜尋結果原始碼取得
    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36",
        'From': 'youremail@domain.com'  
        }

    response = requests.get(urlc,headers=headers).content
    report_soup=BeautifulSoup(response,"html.parser")

    #從原始碼中搜尋10K連結
    links = report_soup.find_all("a",id="documentsbutton")

    link_list=[]

    for link in links:
        aaa=link.get("href")
        link_list.append(aaa)     

    if len(link_list) != 0:   
            
        urlc2="https://www.sec.gov/"+link_list[0]    

        #取得完整財報
        response2 = requests.get(urlc2,headers=headers).content
        report_soup2=BeautifulSoup(response2,"html.parser")

        links2 = report_soup2.find('table',attrs={"class" : "tableFile"}).find_all("a")

        link_list2=[]   
        for link2 in links2:
            bbb=link2.get("href")
            link_list2.append(bbb)

        fin_report="https://www.sec.gov/"+link_list2[0]
        
    #解析財報TXT檔，並找尋所有的Div標籤
        response3 = requests.get(fin_report,headers=headers).content
        try:
            report_soup3=BeautifulSoup(response3,"lxml")

            tag_div=report_soup3.find_all("div")

            #確保Div真的有東西
            if len(tag_div) != 0:   

                #建立兩種標籤剖析(Div/span)，先從span先找，沒有才從DIV直接撈
                div_to_span=[]

                for i in tag_div:

                    try:
                        div_to_span.append(i.find("span").text)
                    except:
                        div_to_span.append(np.nan)

                #從Span裡面找尋有沒有關鍵字
                keyword_search_span=[]

                for tag in div_to_span:

                    tag=str(tag)

                    if str(keyword) in tag:

                        keyword_search_span.append(tag)

                        if len(keyword_search_span)!=0:

                            print(company)
                            print("---"*50)
                            print(len(keyword_search_span))

                            return pd.DataFrame({"Company" : company ,"report link" : fin_report , "Result":keyword_search_span})
                            
                    #Span裡面沒有，再回去div裡面找
                    else:
                                
                        #先將Div標籤取出純文字檔
                        clean_div=[]
                        for i in tag_div:
                    
                            try:
                                clean_div.append(i.text)
                            except:
                                clean_div.append(np.nan)

                        if len(clean_div) !=0 :

                            keyword_search_div=[]

                            for tag in clean_div:

                                tag=str(tag)
                                if str(keyword) in tag:

                                    keyword_search_div.append(tag)

                            print(company)
                            print(len(keyword_search_div))
                            print("---"*50)

                            time.sleep(random.randint(5,10))
                            print("0")

                            if len(keyword_search_div) !=0:

                                return  pd.DataFrame({"Company" : company ,"report link" : fin_report , "Result":keyword_search_div})

                            else:

                                keyword_search_div.append(np.nan)
                                return  pd.DataFrame({"Company" : company ,"report link" : fin_report , "Result": keyword_search_div })
                            
                        else:
                            print("2")

                            return pd.DataFrame({"Company" : company ,"report link" : fin_report , "Result" : "No keyword" })
            else:
                tag_div.append(np.nan)
                return pd.DataFrame({"Company" : company ,"report link" : fin_report , "Result" : tag_div })

        except MemoryError:

            memory=[]
            memory.append("Memory error")
            return pd.DataFrame({"Company" : company ,"report link" : fin_report ,  "Result" : memory })
    else:
        link_list.append("Link wrong")
        result_list=[]
        result_list.append(np.nan)
        return pd.DataFrame({"Company" : company , "report link" : link_list ,  "Result" : result_list})

