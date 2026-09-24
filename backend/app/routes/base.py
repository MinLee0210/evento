from fastapi import APIRouter

base_route = APIRouter()


@base_route.get("/")
async def health() -> dict:
    return {"status": "ok"}
