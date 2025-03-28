from finnhub_apis import basic_fundamentals,get_company_news
from mongo_querries import bulk_insert

async def basic_fundamental_extraction(symbol):
    try:
        data = basic_fundamentals(symbol)
        if not data:
            return None

        years_to_keep = {"2020", "2021", "2022", "2023", "2024", "2025"}

        annual_fields = [
            "bookValue", "cashRatio", "currentRatio", "ebitPerShare", "eps", "ev",
            "fcfMargin", "grossMargin", "inventoryTurnover", "longtermDebtTotalAsset",
            "longtermDebtTotalCapital", "longtermDebtTotalEquity", "netDebtToTotalCapital",
            "netDebtToTotalEquity", "netMargin", "pb", "pe", "roa", "roe", "roic", "rotc", "salesPerShare"
        ]

        quarterly_fields = [
            "bookValue", "cashRatio", "currentRatio", "ebitPerShare", "eps", "fcfMargin",
            "grossMargin", "inventoryTurnover", "longtermDebtTotalAsset", "longtermDebtTotalCapital",
            "longtermDebtTotalEquity", "netDebtToTotalCapital", "netDebtToTotalEquity",
            "netMargin", "pb", "pe", "roa", "roe"
        ]

        resultant_dict = {
            "company_name": symbol,
            "metrics": data.get("metric", {}),
            "series": {
                "annual": {},
                "quarterly": {}
            },
            "years_to_keep": years_to_keep
        }

        # Handle annual data
        annual_series = data.get("series", {}).get("annual", {})
        for field in annual_fields:
            if field in annual_series:
                filtered_data = [
                    entry for entry in annual_series[field]
                    if entry.get("period", "")[:4] in years_to_keep
                ]
                resultant_dict["series"]["annual"][field] = filtered_data

        # Handle quarterly data
        quarterly_series = data.get("series", {}).get("quarterly", {})
        for field in quarterly_fields:
            if field in quarterly_series:
                filtered_data = [
                    entry for entry in quarterly_series[field]
                    if entry.get("period", "")[:4] in years_to_keep
                ]
                resultant_dict["series"]["quarterly"][field] = filtered_data

        await bulk_insert("Company_specific_fundamental_data", [resultant_dict])

        return {"message":"Data inserted successfully"}
    except Exception as e:
        print(f"Error in basic fundamental extraction: {e}")
        return {"error": str(e)}

async def company_news_extraction(company_name,start_date,end_date):
    try:
        data = get_company_news(company_name,start_date,end_date)
        response = await bulk_insert("Company_specific_news_data",data)
        return response
    except Exception as e:
        print(f"Error in company news extraction: {e}")
        return {"error": str(e)}