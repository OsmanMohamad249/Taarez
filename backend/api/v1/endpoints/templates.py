from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()


class TemplateCreate(BaseModel):
    name: str
    description: str | None = None
    payload: dict


class TemplateRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    payload: dict


@router.post("/", response_model=TemplateRead)
async def create_template(item: TemplateCreate):
    # TODO: implement DB create
    return {"id": 0, "name": item.name, "description": item.description, "payload": item.payload}


@router.get("/", response_model=List[TemplateRead])
async def list_templates():
    # TODO: query DB
    return []


@router.get("/{template_id}", response_model=TemplateRead)
async def get_template(template_id: int):
    # TODO: fetch by id
    raise HTTPException(status_code=404, detail="Not implemented")


@router.put("/{template_id}", response_model=TemplateRead)
async def update_template(template_id: int, item: TemplateCreate):
    # TODO: update
    raise HTTPException(status_code=404, detail="Not implemented")


@router.delete("/{template_id}")
async def delete_template(template_id: int):
    # TODO: delete
    return {"ok": True}
