from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import TrackerCreate, TrackerUpdate, TrackerItem
from app.services.auth_service import get_current_user
from app.db.mongo import trackers_col
from bson import ObjectId
from datetime import datetime
from typing import List

router = APIRouter()


def serialize(doc) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.get("/", response_model=List[TrackerItem])
async def get_trackers(user=Depends(get_current_user)):
    cursor = trackers_col.find({"user_id": str(user["_id"])}).sort("created_at", -1)
    return [serialize(doc) async for doc in cursor]


@router.post("/", response_model=TrackerItem)
async def create_tracker(body: TrackerCreate, user=Depends(get_current_user)):
    now = datetime.utcnow()
    doc = {
        **body.dict(),
        "user_id": str(user["_id"]),
        "status": "not_started",
        "created_at": now,
        "updated_at": now,
    }
    result = await trackers_col.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize(doc)


@router.patch("/{tracker_id}", response_model=TrackerItem)
async def update_tracker(tracker_id: str, body: TrackerUpdate, user=Depends(get_current_user)):
    update_data = {k: v for k, v in body.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    result = await trackers_col.find_one_and_update(
        {"_id": ObjectId(tracker_id), "user_id": str(user["_id"])},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return serialize(result)


@router.delete("/{tracker_id}")
async def delete_tracker(tracker_id: str, user=Depends(get_current_user)):
    result = await trackers_col.delete_one(
        {"_id": ObjectId(tracker_id), "user_id": str(user["_id"])}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return {"deleted": True}
