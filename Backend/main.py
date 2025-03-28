
from fastapi import FastAPI, Depends
from mongo import db 
from mongo_querries import find_all,find_one,bulk_insert
from finnhub_apis import get_company_news
from Middleware.basic_fundamentals import basic_fundamental_extraction,company_news_extraction
app = FastAPI()

# Remove this
@app.get("/company_data",tags=["news"])
async def get_all_company_data():
    try:
        return await find_all(collection_name="Company_specific_news_data",projection={"_id": 0},condition={})
    except Exception as e:
        return {"error": str(e)}        
    

@app.get("/company_data/{company_name}",tags=["news"])
async def get_company_data(company_name: str="AAPL"):
    try:
        return await find_one(collection_name="Company_specific_news_data",projection={"_id": 0},condition={"company_name":company_name})
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/company_news",tags=["news"])
async def create_company_news(company_name:str,start_date:str,end_date:str):
    try:
       company_news_extraction(company_name,start_date,end_date)
       return {"message":"Data inserted successfully"}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/basic_fundamentals",tags=["news"])
async def create_basic_fundamentals(symbol:str):
    try:
        data = await basic_fundamental_extraction(symbol)
        if not data:
            return {"error": "No data found"}
        
        return data
    except Exception as e:
        return {"error": str(e)}
