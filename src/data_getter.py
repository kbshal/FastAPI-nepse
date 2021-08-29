import requests
from src.models import Company
from bs4 import BeautifulSoup as bs
import time
import asyncio

class Scrap:
    
    def __init__(self):
        self.headers={
            "Host":"www.nepalstock.com",
            "User-Agent":"Mozilla/5.0 (X11; Linux aarch64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Accept":"ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language":"en-US,en;q=0.5",
            "Accept-Encoding":"gzip, deflate",
            "Content-Type":"application/x-www-form-urlencoded",
            "Content-Length":"52",
            "Origin":"http://www.nepalstock.com",
            "Connection":"keep-alive",
            "Referer":"http://www.nepalstock.com/main/floorsheet/index/6547/?contract-no=&stock-symbol=&buyer=&seller=&_limit=20",
            "Cookie":"ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e341021389a5ee349aafc57cb210c72f%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2289.187.177.75%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A69%3A%22Mozilla%2F5.0+%28X11%3B+Linux+aarch64%3B+rv%3A78.0%29+Gecko%2F20100101+Firefox%2F78.0%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1630139197%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Dceb0ebfc57a2d7699c286acc13699739",
            "Upgrade-Insecure-Requests":"1"
                
                 }
        
        self.payload={
            "contract-no":"",
            "stock-symbol":"",
            "buyer":"",
            "seller":"",
            "_limit":"500",
        } 

    async def get_floorsheet(self,url:str,upto:int) -> list :
        start=time.time()
        companies=[]
        if upto<0 or upto>262:
            return False
        for pagination in range(upto+1):
            skip=0
            url=url+f"{pagination}/"
            res=requests.post(url,headers=self.headers,data=self.payload).content.decode("utf-8")
            souped_data=bs(res,'lxml')
            floor_sheet_table=souped_data.findAll("table",attrs={"class":"table my-table"})[0]
            headers=floor_sheet_table.findAll("tr",{"class":"unique"})[0]
            for tds in floor_sheet_table.findAll('tr'):
                if skip<2:
                    skip+=1
                    continue
                else:
                    try:
                        
                        json_template={

                            "contract":None,
                            "symbool":None,
                            "buyer broker":None,
                            "seller broker":None,
                            "quantity":None,
                            "rate":None,
                            "amount":None
                        }

                        fsv=tds.findAll("td")
                        company=Company()
                        company.contract=fsv[1].getText()
                        company.symbool=fsv[2].getText()
                        company.buyer_broker=fsv[3].getText()
                        company.seller_broker=fsv[4].getText()
                        company.quantity=fsv[5].getText()
                        company.rate=fsv[6].getText()
                        company.amount=fsv[7].getText()
                        json_template["contract"]=company.contract
                        json_template["symbool"]=company.symbool
                        json_template["buyer broker"]=company.buyer_broker
                        json_template["seller broker"]=company.seller_broker
                        json_template["quantity"]=company.quantity
                        json_template["rate"]=company.rate
                        json_template["amount"]=company.amount
                        companies.append(json_template)
                        del json_template
                        del company
                    except IndexError:
                        break
            
        companies.append({"Total time taken":time.time()-start})
        return companies
      

