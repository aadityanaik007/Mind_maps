from fastapi import APIRouter
from mongo_querries import find_all, find_one
from Middleware.basic_fundamentals import (
    basic_fundamental_extraction,
    company_news_extraction,
)

router = APIRouter(tags=["News"])

@router.get("/get_all_tickers")
async def get_all_tickers():
    try:
        return ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'NFLX', 'NVDA', 'INTC', 'AMD']
    except Exception as e:
        return {"error": str(e)}


@router.get("/company_data")
async def get_all_company_data():
    try:
        return await find_all(
            collection_name="Company_specific_news_data",
            projection={"_id": 0},
            condition={}
        )
    except Exception as e:
        return {"error": str(e)}


@router.get("/company_news")
async def get_company_news(ticker: str = "AAPL"):
    try:
        return await find_all(
            collection_name="Company_specific_news_data",
            projection={"_id": 0},
            condition={"company_name": ticker}
        )
    except Exception as e:
        return {"error": str(e)}


@router.get("/company_data/{company_name}")
async def get_company_data(company_name: str = "AAPL"):
    try:
        return await find_one(
            collection_name="Company_specific_news_data",
            projection={"_id": 0},
            condition={"company_name": company_name}
        )
    except Exception as e:
        return {"error": str(e)}


@router.post("/company_news")
async def create_company_news(company_name: str, start_date: str, end_date: str):
    try:
        response = await company_news_extraction(company_name, start_date, end_date)
        return {"message": response}
    except Exception as e:
        return {"error": str(e)}


@router.post("/basic_fundamentals")
async def create_basic_fundamentals(symbol: str):
    try:
        data = await basic_fundamental_extraction(symbol)
        if not data:
            return {"error": "No data found"}
        return data
    except Exception as e:
        return {"error": str(e)}

@router.get("/sidebar_data")
async def sidebar_data():
    try:
        sidebar_info = [
            "Fundamental Data",
            "News Data",
            "Mergers and Acquisitions",
        ]
        return sidebar_info
    except Exception as e:
        return {"error": str(e)}