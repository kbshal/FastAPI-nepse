from fastapi import FastAPI,Query,Path,HTTPException,status,Body,Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.encoders import jsonable_encoder
from src.models import Configuration,Source,MyException
from src.data_getter import Scrap
from typing import Optional
import uuid


app=FastAPI(title="Nepse API",description="Nepse api which can provide floorsheet data. It provides floorsheet by scraping the nepse website")


# exception handler

@app.exception_handler(MyException)
async def myexception(request:Request,exception:MyException):
    return JSONResponse(
        status_code=418,
        content={"message":f"Oops! {exception.name} did something. Please contact system admin! "},
    )

@app.get("/",response_class=HTMLResponse,tags=["Homepage"])
async def homepage():
    content="""
    <a href="https://nepsegodapi.herokuapp.com/floorsheet?upto=1"> Click here</a>

    """
    return content

 
@app.post("/floorsheet_post",status_code=status.HTTP_201_CREATED,tags=['POST method at this endpoint'])
async def post_floorsheet(config:Configuration=Body(None),upto:Optional[int]=Query(None)):
    configs=jsonable_encoder(config)
    if upto:
        scrapper=Scrap()
        result=await scrapper.get_floorsheet(Source.url.value,upto)
        print("Done! from upto query") # for debug 
        if result is False:
            raise HTTPException(status_code=status.HTTP_201_CREATED,detail="Error occured please contact system admin")
    
    # check fo upto query parameter

    if not upto:
        scrapper=Scrap()
        result=await scrapper.get_floorsheet(Source.url.value,1)
        if result is False:
            raise HTTPException(status_code=status.HTTP_201_CREATED,detail="Error occured please contact system admin")
    
    # filter according to the user request body model
    
    if config:
        filtered=None
        for i in result:
            try:
                if (configs["contract_no"]==i["contract"]) or (configs["symbool"]==i["symbool"]):
                    filtered=i
                    return filtered
                else:
                    continue
            except KeyError: # to counter error caused by 1000th item
                pass
    try:
        if filtered is None:
            return result
        elif filtered:
            return filtered
    except NameError:
        return result



@app.get("/floorsheet",status_code=status.HTTP_201_CREATED,tags=['GET method at this endpoint'])
async def get_floorsheet(upto:Optional[int]=Query(None)):
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

    


    

