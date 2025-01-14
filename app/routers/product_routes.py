from fastapi import APIRouter, Response, Depends

from sqlmodel import Session

from app.schemas.products import ProductInSchema, ProductOutSchema, CategoryInSchema, CategoryOutSchema
from app.db.models.product import Category, Product
from app.db.session import get_db

product_router = APIRouter(
    prefix='/product'
)

@product_router.post('/categories/create/')
def create_category(category: CategoryInSchema, db: Session = Depends(get_db)):
    category = Category(**category.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return Response({"message": "Category Added Successfully"})


@product_router.get('/categories/get')
async def get_categories():
    return {"message": "orders"}