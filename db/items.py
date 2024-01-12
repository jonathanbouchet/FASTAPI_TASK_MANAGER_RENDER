from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from db.core import DBItem, NotFoundError

class Item(BaseModel):
    id: int = Field(description="the ID of the item")
    name: str = Field(description="the name of the item")
    description: str | None = Field(None, description="the description of an item")


class ItemCreate(BaseModel):
    name: str = Field(description="the name of the item")
    description: str | None = Field(None, description="the description of an item")


class ItemUpdate(BaseModel):
    name: str = Field(description="the name of the item")
    description: str | None = Field(None, description="the description of an item")


def read_db_items(session: Session) -> list[DBItem]:
    db_items = session.query(DBItem).all()
    print(f"db_items:{db_items}, type: {type(db_items)}")
    return db_items


def read_db_item(item_id: int, session: Session) -> DBItem:
    db_item = session.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise NotFoundError(f"Item with id {item_id} not found.")
    return db_item


def create_db_item(item: ItemCreate, session: Session) -> DBItem:
    db_item = DBItem(**item.model_dump(exclude_none=True))
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def update_db_item(item_id: int, item: ItemUpdate, session: Session) -> DBItem:
    db_item = read_db_item(item_id, session)
    for key, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, key, value)
    session.commit()
    session.refresh(db_item)
    return db_item


def delete_db_item(item_id: int, session: Session) -> DBItem:
    db_item = read_db_item(item_id, session)
    session.delete(db_item)
    session.commit()
    return db_item
