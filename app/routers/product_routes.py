from fastapi import APIRouter, Response, Depends

from sqlmodel import Session, select

from app.schemas.products import ProductInSchema, ProductOutSchema, CategoryInSchema, CategoryOutSchema
from app.db.models.product import Category, Product
from app.db.session import get_db
from app.utils.model_utilty import generate_slug

product_router = APIRouter(
    prefix='/product'
)

@product_router.post('/categories/create/')
def create_category(category: CategoryInSchema, db: Session = Depends(get_db)):
    category.slug = generate_slug(category.name)
    category = Category(**category.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return Response({"message": "Category Added Successfully"})


@product_router.get('/categories/get/', response_model=list[CategoryOutSchema])
async def get_categories(db: Session = Depends(get_db)) -> list[CategoryOutSchema]:
    statement = select(Category)
    categories = db.exec(statement)
    return categories

