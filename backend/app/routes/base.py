from fastapi import APIRouter, Request

from api.v1.base import generate_quote

base_route = APIRouter()

@base_route.get("/")
async def get_landing_page(request: Request): 
    try: 
        quote = generate_quote()
    except: 
        quote = """"He who would learn to fly one day must first learn to stand and walk and run and climb and dance; one cannot fly into flying." — Nietzsche"""
    return quote