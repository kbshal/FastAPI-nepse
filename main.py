from fastapi import FastAPI,Query,Path,HTTPException,status,Body,Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.encoders import jsonable_encoder
from src.models import Configuration,Source,MyException
from src.data_getter import Scrap
from typing import Optional
import uuid


app=FastAPI(title="API for nepse",description="Can provide floorsheet data ")



@app.exception_handler(MyException)
async def myexception(request:Request,exception:MyException):
    return JSONResponse(
        status_code=418,
        content={"message":f"Oops! {exception.name} did something. Please contact system admin! "},
    )

@app.get("/",response_class=HTMLResponse,tags=["homepage"])
async def homepage():
    content="""
    <a href="https://nepsegodapi.herokuapp.com/floorsheet?upto=1"> Click here</a>

    """
    return content

@app.get("/floorsheet",status_code=status.HTTP_201_CREATED,tags=["floorsheet"])
async def get_floorsheet(config:Configuration=Body(None,examples={}),upto:Optional[int]=Query(None)):
    configs=jsonable_encoder(config)
    if upto:
        scrapper=Scrap()
        result=await scrapper.get_floorsheet(Source.url.value,upto)
        if result is False:
            raise HTTPException(status_code=status.HTTP_201_CREATED,detail="Error occured please contact system admin")

    if not upto:
        scrapper=Scrap()
        result=await scrapper.get_floorsheet(Source.url.value,1)
        if result is False:
            raise HTTPException(status_code=status.HTTP_201_CREATED,detail="Error occured please contact system admin")
    
    return result

    


    

