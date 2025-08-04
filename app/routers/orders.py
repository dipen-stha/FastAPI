from typing import Annotated

from sqlmodel import Session
from starlette.responses import JSONResponse

from app.db.crud import create_order, get_all_user_orders, get_user_orders_by_id, count_orders_status, \
    count_each_users_orders
from app.db.session import get_db
from app.schemas.filters import OrderFilter
from app.schemas.orders import UserOrderIn, UserOrderOut, OrderStatSchema

from fastapi import APIRouter, Depends, Query, Response, status

from app.schemas.user import UserOrderStats

order_router = APIRouter(prefix="/orders")


@order_router.get("/get/all/", tags=["User Order"], response_model=list[UserOrderOut])
def fetch_list_user_orders(
    db: Annotated[Session, Depends(get_db)],
    filter_query: Annotated[Query, Depends(OrderFilter)],
):
    try:
        user_orders = get_all_user_orders(db, filter_query)
        return user_orders
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)}
        )


@order_router.get(
    "/get/{user_id}/", tags=["User Order"], response_model=list[UserOrderOut]
)
def fetch_user_order(
    db: Annotated[Session, Depends(get_db)],
    user_id: int,
):
    try:
        user_orders = get_user_orders_by_id(user_id, db)
        user_orders_data = [user_order.model_dump() for user_order in user_orders]
        return Response(
            status_code=status.HTTP_200_OK, content={"data": user_orders_data}
        )
    except Exception as e:
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)}
        )


@order_router.post("/create/", tags=["User Order"], response_model=UserOrderOut)
def create_user_order(db: Annotated[Session, Depends(get_db)], data: UserOrderIn):
    try:
        created_instance = create_order(data, db)
        return created_instance
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)}
        )


@order_router.get("/stats/", tags=["User Order"], response_model=OrderStatSchema)
def get_order_stats(db: Annotated[Session, Depends(get_db)]):
    try:
        stats_data = count_orders_status(db)
        return stats_data
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

@order_router.get("/user-stats/", tags=["User Order"], response_model=list[UserOrderStats])
def get_user_order_stats(db: Annotated[Session, Depends(get_db)]):
    try:
        user_stats = count_each_users_orders(db)
        return user_stats
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})