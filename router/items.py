from fastapi import APIRouter, HTTPException, Request, Depends, status
from sqlalchemy.orm import Session
from db.core import get_db, NotFoundError
from db.items import (
    Item,
    ItemCreate,
    ItemUpdate,
    read_db_item,
    read_db_items,
    create_db_item,
    update_db_item,
    delete_db_item
)
from .limit import limiter

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
@limiter.limit("10/minute")
async def read_all_items(request: Request, db: Session = Depends(get_db)) -> list[Item]:
    try:
        db_items = read_db_items(db)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
    return [Item(**db_item.__dict__) for db_item in db_items]


@router.get("/{item_id}")
async def read_item(request: Request, item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        db_item = read_db_item(item_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item ID {item_id} not found") from e
    return Item(**db_item.__dict__)


@router.post("/")
async def create_item(request: Request, item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    db_item = create_db_item(item, db)
    return Item(**db_item.__dict__)


@router.put("/{item_id}")
def update_item(request: Request, item_id: int, item: ItemUpdate, db: Session = Depends(get_db)) -> Item:
    try:
        db_item = update_db_item(item_id, item, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=f"item ID {item_id} not found") from e
    return Item(**db_item.__dict__)


@router.delete("/{item_id}")
def delete_item(request: Request, item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        db_item = delete_db_item(item_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=f"item ID {item_id} not found") from e
    return Item(**db_item.__dict__)

