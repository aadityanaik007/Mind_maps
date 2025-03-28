from mongo import db

async def find_all(collection_name, condition={},projection={"_id":0}):
    collection = db[collection_name]
    cursor = collection.find(condition,projection)
    data = await cursor.to_list(length=100)
    return data

async def find_one(collection_name, condition={},projection={"_id":0}):
    collection = db[collection_name]
    document = await collection.find_one(condition, projection)
    return document

async def bulk_insert(collection_name, data):
    try:
        collection = db[collection_name]
        await collection.insert_many(data)
        return {"message":"Data inserted successfully"}
    except Exception as e:
        print(f"Error inserting data: {e}")
        return {"Error":f"{str(e)}"}