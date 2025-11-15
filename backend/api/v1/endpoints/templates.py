from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.database import get_db
from models.template import Template as TemplateModel

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


@router.post("/", response_model=TemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(item: TemplateCreate, db: Session = Depends(get_db)):
    # ensure unique name
    existing = db.query(TemplateModel).filter(TemplateModel.name == item.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Template with this name already exists")
    tmpl = TemplateModel(name=item.name, description=item.description, payload=item.payload)
    db.add(tmpl)
    db.commit()
    db.refresh(tmpl)
    return TemplateRead(id=tmpl.id, name=tmpl.name, description=tmpl.description, payload=tmpl.payload)


@router.get("/", response_model=List[TemplateRead])
def list_templates(db: Session = Depends(get_db)):
    items = db.query(TemplateModel).all()
    return [TemplateRead(id=i.id, name=i.name, description=i.description, payload=i.payload) for i in items]


@router.get("/{template_id}", response_model=TemplateRead)
def get_template(template_id: int, db: Session = Depends(get_db)):
    tmpl = db.query(TemplateModel).get(template_id)
    if not tmpl:
        raise HTTPException(status_code=404, detail="Template not found")
    return TemplateRead(id=tmpl.id, name=tmpl.name, description=tmpl.description, payload=tmpl.payload)


@router.put("/{template_id}", response_model=TemplateRead)
def update_template(template_id: int, item: TemplateCreate, db: Session = Depends(get_db)):
    tmpl = db.query(TemplateModel).get(template_id)
    if not tmpl:
        raise HTTPException(status_code=404, detail="Template not found")
    # check name uniqueness
    if item.name != tmpl.name:
        other = db.query(TemplateModel).filter(TemplateModel.name == item.name).first()
        if other:
            raise HTTPException(status_code=400, detail="Template with this name already exists")
    tmpl.name = item.name
    tmpl.description = item.description
    tmpl.payload = item.payload
    db.add(tmpl)
    db.commit()
    db.refresh(tmpl)
    return TemplateRead(id=tmpl.id, name=tmpl.name, description=tmpl.description, payload=tmpl.payload)


@router.delete("/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    tmpl = db.query(TemplateModel).get(template_id)
    if not tmpl:
        raise HTTPException(status_code=404, detail="Template not found")
    db.delete(tmpl)
    db.commit()
    return {"ok": True}
