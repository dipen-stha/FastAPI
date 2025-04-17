from fastapi import APIRouter, Response, Depends, Request
from sqlalchemy.exc import NoResultFound

from sqlmodel import Session, select
from starlette import status
from starlette.responses import JSONResponse

from app.schemas.products import ProductInSchema, ProductOutSchema, CategoryInSchema, CategoryOutSchema
from app.db.models.product import Category, Product
from app.db.models.user import User
from app.db.session import get_db
from app.services.permissions import PermissionChecker
from app.utils.model_utilty import generate_slug, update_model_instance

product_router = APIRouter(
    prefix='/product'
)

@product_router.post('/categories/create/', response_model=CategoryOutSchema)
def create_category(category: CategoryInSchema, db: Session = Depends(get_db)):
    data = category.model_dump()
    data['slug'] = generate_slug(db, Category, category.name)
    category = Category(**data)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@product_router.get('/categories/get/', response_model=list[CategoryOutSchema])
async def get_categories(
        request: Request,
        user_permissions:User = Depends(PermissionChecker(required_permissions=["can-access-all"])),
        db: Session = Depends(get_db)) -> list[CategoryOutSchema]:
    statement = select(Category)
    categories = db.exec(statement)
    return categories


@product_router.put('/categories/update/{category_id}/', response_model=CategoryOutSchema)
async def update_category(
        category_id: int,
        category: CategoryInSchema,
        db: Session = Depends(get_db),
        user_permission: User = Depends(PermissionChecker(required_permissions=["can-update-all"])),
):
    try:
        category_obj = db.exec(select(Category).where(Category.id == category_id)).first()
        if not category_obj:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Category not found"})
        data = category.model_dump(exclude_unset=True)
        data['slug'] = generate_slug(db, Category, category.name)
        updated_category = update_model_instance(data, category_obj)
        db.add(updated_category)
        db.commit()
        db.refresh(updated_category)
        return updated_category
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})
