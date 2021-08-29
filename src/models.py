from pydantic import BaseModel
from typing import Optional
from enum import Enum


class MyException(Exception):
    def __init__(self,name:str):
        self.name=name

class Company:
    def __init__(self,contract=None):
        self.contract_no=contract
        self.symbool=None
        self.buyer_broker=None
        self.seller_broker=None
        self.quantity=None
        self.rate=None
        self.amount=None


class Source(str,Enum):
    url="http://www.nepalstock.com/main/floorsheet/index/"

class Configuration(BaseModel):
    symbool:str
    contract_no:int
      
    class Config:
        extra_schema={
            "example":{
                "symbool":"PMLI",
                "contract_no":2021051203
            }
        }

