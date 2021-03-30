from fastapi import APIRouter, Body, Depends, HTTPException

router = APIRouter()


@router.post("/login")
async def login():
    pass


@router.get("/login")
async def login():
    pass
