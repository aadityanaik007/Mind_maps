from mongo import db
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import BulkWriteError
import math

async def find_all(collection_name, condition={},projection={"_id":0}):
    collection = db[collection_name]
    cursor = collection.find(condition,projection)
    data = await cursor.to_list(length=100)
    return data

async def find_one(collection_name, condition={},projection={"_id":0}):
    collection = db[collection_name]
    document = await collection.find_one(condition, projection)
    return document

async def bulk_insert(collection_name, data, chunk_size=500):
    collection = db[collection_name]
    total_inserted = 0
    chunk_count = math.ceil(len(data) / chunk_size)

    for i in range(chunk_count):
        chunk = data[i * chunk_size : (i + 1) * chunk_size]

        # Remove any _id fields to avoid duplicate key errors
        for doc in chunk:
            doc.pop("_id", None)

        try:
            await collection.insert_many(chunk, ordered=False)
            total_inserted += len(chunk)
            print(f"✅ Inserted chunk {i+1}/{chunk_count}, total inserted: {total_inserted}")

        except BulkWriteError as bwe:
            # Remove duplicate _id documents and retry
            duplicate_ids = {
                error["op"].get("_id")
                for error in bwe.details.get("writeErrors", [])
                if error.get("code") == 11000
            }

            cleaned_chunk = [
                doc for doc in chunk if doc.get("_id") not in duplicate_ids
            ]

            if cleaned_chunk:
                try:
                    await collection.insert_many(cleaned_chunk, ordered=False)
                    total_inserted += len(cleaned_chunk)
                    print(f"♻️ Cleaned and re-inserted chunk {i+1}: {len(cleaned_chunk)} docs")
                except Exception as retry_error:
                    print(f"❌ Retry failed for chunk {i+1}: {retry_error}")
            else:
                print(f"⚠️ All docs in chunk {i+1} were duplicates or bad — skipped.")

        except Exception as general_error:
            print(f"❌ Unhandled error in chunk {i+1}: {general_error}")

    return {"message": f"✅ Bulk insert completed. Total inserted: {total_inserted}"}
