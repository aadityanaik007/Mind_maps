
from typing import Union

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from mongo import db 
from mongo_querries import find_all,find_one,bulk_insert
from finnhub_apis import get_company_news,get_general_news,get_ohlc_data
app = FastAPI()

def get_db():
    return db

@app.get("/news",tags=["news"])
async def get_news(db=Depends(get_db)):
    docs = db["news"].find()
    results = await docs.to_list(length=10)
    return results

# Remove this
@app.get("/company_data",tags=["news"])
async def get_all_company_data():
    try:
        return await find_all(collection_name="Company_specific_data",projection={"_id": 0},condition={})
    except Exception as e:
        return {"error": str(e)}        
    

@app.get("/company_data/{company_name}",tags=["news"])
async def get_company_data(company_name: str="AAPL"):
    try:
        return await find_one(collection_name="Company_specific_data",projection={"_id": 0},condition={"company_name":company_name})
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/news",tags=["news"])
async def create_news(company_name:str,start_date:str,end_date:str,db=Depends(get_db)):
    try:
        data = get_company_news(company_name,start_date,end_date)
        response = await bulk_insert("Company_specific_data",data)
        return response
    except Exception as e:
        return {"error": str(e)}
