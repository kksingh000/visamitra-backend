from fastapi import APIRouter, HTTPException
from app.models.schemas import VisaQuery, VisaResponse
from app.services.visa_service import get_corridor, get_ai_tips

router = APIRouter()


@router.post("/check", response_model=VisaResponse)
async def check_visa(body: VisaQuery):
    corridor = get_corridor(body.from_country, body.to_country, body.purpose)
    if not corridor:
        raise HTTPException(
            status_code=404,
            detail=f"Corridor {body.from_country}-{body.to_country} ({body.purpose}) not yet supported."
        )

    ai_tips = None
    if body.occupation:
        ai_tips = await get_ai_tips(corridor, body.occupation, body.duration_days)

    return {**corridor, "ai_tips": ai_tips}


@router.get("/corridors")
async def list_corridors():
    from app.services.visa_service import load_data
    data = load_data()
    return {"corridors": list(data.keys()), "count": len(data)}
