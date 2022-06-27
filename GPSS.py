import requests
import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup 
from datetime import date, datetime


#申請("application-reference")/公告("publication-reference")的日期["Date"]及文件["Doc"]函數
def doc_date(data,item):

    target=data.find(item)
    if target!=None:

        datedoc_list=[]
        target_date=target.find("date")
        target_doc=target.find("doc-number")

        if target_date !=None:

            datedoc_list.append(str(target_date.string))
        else:
            datedoc_list.append(np.nan)

        if target_doc !=None:

            datedoc_list.append(str(target_doc.string))
        else:
            datedoc_list.append(np.nan)
        
        result={"Date":datedoc_list[0],"Doc":datedoc_list[1]}

        return result

    else:

        return {"Date":np.nan,"Doc":np.nan}

# 申請("applicant")/發明人("inventor")函數
def get_name(data,item):

    targets=data.select(item)

    if len(targets)!=0:

        names=[]
        for target in targets:

            name=[]
            target_orginal=target.find("name")
            target_name_eng=target.find("english-name")
            target_country=target.find("country-code")

            if target_orginal!=None:
                name.append(str(target_orginal.string))
            else:
                name.append(np.nan)

            if target_name_eng!=None:
                name.append(str(target_name_eng.string))
            else:
                name.append(np.nan)

            if target_country!=None:
                name.append(str(target_country.string))
            else:
                name.append(np.nan)

            names.append(name)

        return names

#代理人函數
def get_agent(data):

    targets=data.select("agent")

    names=[]
    for target in targets:

        names.append(str(target.string))

    if len(names) != 0:

        return names

    else:          

        return np.nan

#摘要函數
def get_abstract(data):
    abstracts=data.find("abstract")

    abstract_list=[]
    if abstracts!=None:
        abstract=abstracts.select("p")
        
        for abs in abstract:
            
            abstract_list.append(str(abs.string))

        return abstract_list

#優先權函數
def get_priority(data):
    priorities=data.find("priority-claims")

    priorities_list=[]

    if priorities!=None:

        priorities=priorities.select("priority-claim")

        for priority in priorities:

            priority_list=[]

            priority_country=priority.find("country")
            priority_date=priority.find("date")
            priority_number=priority.find("doc-number")

            if priority_country!=None:
                priority_list.append(str(priority_country.string))
            else:
                priority_list.append(np.nan)

            if priority_date!=None:
                priority_list.append(str(priority_date.string))
            else:
                priority_list.append(np.nan)

            if priority_number!=None:
                priority_list.append(str(priority_number.string))
            else:
                priority_list.append(np.nan)

            priorities_list.append(priority_list)

            if len(priorities_list) == 0:
                priorities_list.append(np.nan)

        return priorities_list

#專利名稱[title]及專利英文名稱["title_eng"]函數
def get_title(data):

    name=[]
    patent_title=data.find("patent-title")

    if patent_title !=None:

        title_name=patent_title.find("title")
        title_name_eng=patent_title.find("english-title")

        if title_name!=None:
            name.append(str(title_name.string))
        else:
            name.append(np.nan)

        if title_name_eng!=None:
            name.append(str(title_name_eng.string))
        else:
            name.append(np.nan)

        return{"title":name[0],"title_eng":name[1]}

    else:

        return{"title":np.nan,"title_eng":np.nan}

#引用專利搜尋函數
def get_citation(data):

    references=data.find("references-cited")

    reference_list=[]

    if references!=None:
        references=references.select("citation")

        for reference in references:
            reference_list.append(str(reference.string))

        return reference_list

    else:
        return np.nan

# #IPC/LOC/CPC/FI/F-term/D-term/USPC(各模型以小寫啟動)搜尋函數
def get_classification(data,model):

    if model == "ipc":
                
        all_ipcs=data.find("classifications-ipc")

        ipc_list=[]

        if all_ipcs != None:
            ipcs=all_ipcs.select("ipc")
            
            for ipc in ipcs:
                ipc_list.append(str(ipc.string))

            return ipc_list

        else:
            return np.nan        

    elif model == "loc":

        all_locs=data.find("classifications-loc")

        loc_list=[]
        if all_locs != None:
            locs=all_locs.select("loc")

            if locs != None:

                for loc in locs:
                    loc_list.append(str(loc.string))

                return loc_list

            else:
                return np.nan

        else:
            return np.nan

    elif model == "cpc":

        all_cpcs=data.find("classifications-cpc")
        cpc_list=[]

        if all_cpcs!=None:
            cpcs=all_cpcs.select("cpc")

            for cpc in cpcs:
                cpc_list.append(str(cpc.string))

            if len(cpc_list) != 0:

                return cpc_list

            else:
                return np.nan

        else:
            return np.nan

    elif model == "fi":
        all_terms=data.find("classifications-national")

        fi_list=[]
        if all_terms != None:

            FIs=all_terms.select("fi")

            for fi in FIs:
                fi_list.append(str(fi.string))

            if len(fi_list) != 0:

                return fi_list

            else:
                return np.nan

        else:
            return np.nan

    elif model == "f-term":
        all_terms=data.find("classifications-national")

        f_term_list=[]
        if all_terms != None:

            F_terms=all_terms.select("f-term")

            for F_term in F_terms:
                f_term_list.append(str(F_term.string))
            
            if len(f_term_list) !=0:

                return f_term_list

            else:
                return np.nan

        else:
            return np.nan

    elif model == "d-term":

        all_terms=data.find("classifications-national")

        d_term_list=[]
        if all_terms != None:

            d_terms=all_terms.select("d-term")

            for d_term in d_terms:
                d_term_list.append(str(d_term.string))
            
            if len(d_term_list) !=0:

                return d_term_list
            else:
                return np.nan

        else:
            return np.nan

    elif model == "uspc":
        all_terms=data.find("classifications-national")

        uspc_term_list=[]
        if all_terms != None:

            uspcs=all_terms.select("uspc")

            for uspc in uspcs:
                uspc_term_list.append(str(uspc.string))            

            if len(uspc_term_list) != 0:

                return uspc_term_list

            else:
                return np.nan
            
        else:
             return np.nan

#此函數用來清理TEJ原始檔案的日期
def get_nodesh(target):
    
    if pd.isna(target) == False:
        
        target_string=target.strftime('%Y%m%d')

        return target_string

    else:

        return np.nan

#此函數用來還原成時間，以利年份抓取
def get_timeback(target_string):
    
    if pd.isna(target_string) == False:
        
        target_time=datetime.strptime(target_string, "%Y%m%d")
        target_year=target_time.year

        return target_year

    else:

        return np.nan

#移除英文名後面雜名用的函數
def get_clean_company_name(targets,stopword):

    clean_name=[]

    targets=targets.replace(",","")
    targets=targets.replace(".","")
    targets=targets.replace("&","")
    targets=targets.upper()

    for target in targets.split():
        
        if target not in  stopword :

            clean_name.append(target)


    final_name=" ".join(clean_name)


    return final_name

#用來取得所有申請人的筆數
def get_applicant_number(targets):

    if targets != None:

        return int(len(targets))

    else:

        return np.nan

#用來取得IPC一系列的筆數
def get_IPC_number(targets):

    if type(targets) != float:

        if pd.isna(targets).any() == False:

            return int(len(targets))

        else:

            return np.nan

    else:

        return np.nan

#用來取得所有內涵多重資訊者(包含:申請人/發明人)
def finish_patent_multiple(order,target):

    if target != None:

        if  order <= len(target) :

            name = target[order - 1][1]            
            country = target[order - 1][2]

            return {"Name" : name , "Country" : country}
            
        else:

            return {"Name" : np.nan , "Country" : np.nan}

    else:

        return {"Name" : np.nan , "Country" : np.nan}

#優先權需回傳3項，另外寫
def finish_patent_multiple_3(order,target):

    if target != None:

        if  order <= len(target) :

            country = target[order - 1][0]
            date = target[order - 1][1]            
            doc = target[order - 1][2]

            return {"Doc" : doc , "Country" : country , "Date" : date}
            
        else:

            return {"Doc" : np.nan , "Country" : np.nan , "Date" : np.nan}

    else:

        return {"Doc" : np.nan , "Country" : np.nan , "Date" : np.nan}

#用來取得內涵單一資訊者(包含:引用專利/IPC/LOC/CPC/USPC/FI/F-term/D-term)
def finish_patent_single(order,target):

    if type(target) != float:

        if order <= len(target) :

            return target[order - 1]

        else:

            return np.nan

    else:

        return np.nan

      
#最終爬蟲函數
def gpss_crawler(company,start_day,usercode):

    #將搜尋條件與公司名合併，並進行網頁存取，先回傳一筆，以了解目前最新專利筆數
    company_address=str("https://gpss1.tipo.gov.tw/gpsskmc/gpss_api?userCode="+str(usercode)+"&patDB=TWA,TWB,TWD,JPA,JPB,JPD,CNA,CNB,CND,KPA,KPB,KPD,USA,USB,USD,SEAA,SEAB,WO,EPA,EPB,EUIPO,OTA,OTB&patAG=A,B&patTY=I,M,D&AX="+company+"&ID="+str(start_day)+":20211231&expFld=PN,AN,ID,AD,TI,PA,IN,LX,EX,PR,AB,IC,IQ,CS,UC,FI,FT,IR,CI,CL&expFmt=xml&expQty=1")
    respone_xml = requests.get(company_address)

    #網頁解析，並確認有無專利資料，無專利資料者存在message標籤
    respone_soup=BeautifulSoup(respone_xml.content,"html.parser")
    patent_exist=respone_soup.select("message")
    total_rec=respone_soup.find("total-rec")

    #如果不存在message，且存在專利數據者，再次存取並開始抓專利資料
    if len(patent_exist) == 0 and total_rec != None:

        if int(total_rec.string) >0:

            new_quantity=total_rec.string                

            #以最新的專利筆數進行存取
            company_address=str("https://gpss1.tipo.gov.tw/gpsskmc/gpss_api?userCode="+str(usercode)+"&patDB=TWA,TWB,TWD,JPA,JPB,JPD,CNA,CNB,CND,KPA,KPB,KPD,USA,USB,USD,SEAA,SEAB,WO,EPA,EPB,EUIPO,OTA,OTB&patAG=A,B&patTY=I,M,D&AX="+company+"&ID="+str(start_day)+":20211231&expFld=PN,AN,ID,AD,TI,PA,IN,LX,EX,PR,AB,IC,IQ,CS,UC,FI,FT,IR,CI,CL&expFmt=xml&expQty=" + str(new_quantity))
            respone_xml = requests.get(company_address)

            #網頁解析再次確認有無message，因為若超出下載量會再次出現message
            respone_soup=BeautifulSoup(respone_xml.content,"html.parser")
            patent_exist=respone_soup.select("message")

            if len(patent_exist) == 0:

                print(company)

                #從最外層的節點patentcontent開始往內找，此處應為另一個迴圈，用以抓取全部專利的資料
                patent_data=respone_soup.select("patentcontent")

                #維持表格檢索的呈現方式:
                #申請日/公告日/申請號/公告號/證書號/申請人/發明人/代理人/優先權/專利名稱/摘要/引用專利/引用非專利/被參考次數/IPC/LOC/CPC/USPC/原件影像/FI/F-Term/D-Term/命中次數/公報卷期
                result=[]
                for i in range(len(patent_data)):

                    print(i+1)

                    patent_data_2=patent_data[i]
                    
                    #test 最外層為tuple即()，如此一來便為固定值，無法變化，再裝進List中，才能匯進Dataframe
                    test=(company,i+1,doc_date(patent_data_2,"application-reference")["Date"],doc_date(patent_data_2,"publication-reference")["Date"],\
                        doc_date(patent_data_2,"application-reference")["Doc"],doc_date(patent_data_2,"publication-reference")["Doc"],\
                        get_name(patent_data_2,"applicant"),get_name(patent_data_2,"inventor"),get_agent(patent_data_2),get_priority(patent_data_2),\
                        get_title(patent_data_2)["title"],get_title(patent_data_2)["title_eng"],get_abstract(patent_data_2),get_citation(patent_data_2),\
                        get_classification(patent_data_2,"ipc"),get_classification(patent_data_2,"loc"),get_classification(patent_data_2,"cpc"),\
                        get_classification(patent_data_2,"uspc"),get_classification(patent_data_2,"fi"),get_classification(patent_data_2,"f-term"),\
                        get_classification(patent_data_2,"d-term"))

                    result.append(test)


                final=pd.DataFrame(result,columns=["公司英文名","序號","申請日","公告日","申請號","公告號","申請人",\
                    "發明人","代理人","優先權","專利名稱","專利英文名稱","摘要",\
                    "引用專利","IPC","LOC","CPC","USPC","FI","F-term","D-term"])

                return final
            
            else:

                return "超出存取筆數"

        else:

            return "超出存取筆數"
            
    else:

        return "超出存取筆數"



