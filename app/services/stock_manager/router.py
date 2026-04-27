"""Router du module stock_manager."""
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.configs.database import get_db
from app.services.stock_manager.handler import create_product, update_product
from app.services.stock_manager.schemas import ProductCreateSchema, ProductResponseSchema, ProductUpdateSchema

router = APIRouter(prefix="/stock_manager", tags=["stock_manager"])

@router.post("/product", response_model=ProductResponseSchema, status_code=201)
async def register_product_path(data: ProductCreateSchema, db: AsyncSession = Depends(get_db)):
    print ('router ok✅')
    return await create_product(db, data)

@router.patch("/products/{product_id}",response_model=ProductResponseSchema)
async def update_product_path(
    product_id: UUID,
    data: ProductUpdateSchema,
    db: AsyncSession = Depends(get_db)
):
    return await update_product(product_id , data , db)