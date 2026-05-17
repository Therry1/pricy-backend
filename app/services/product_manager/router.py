"""Router du module product_manager."""
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.configs.database import get_db
from app.services.product_manager.handler import constitute_new_product, create_product, get_one_product, get_products, update_product
from app.services.product_manager.schemas import ConstituateProductSchema, ListProductResponseSchema, ProductCreateSchema, ProductResponseSchema, ProductUpdateSchema

router = APIRouter(prefix="/product_manager", tags=["product_manager"])

# fonction de création d'un produit dans le système
@router.post("/product", response_model=ProductResponseSchema, status_code=201)
async def register_product_path(data: ProductCreateSchema, db: AsyncSession = Depends(get_db)):
    print ('router ok✅')
    return await create_product(db, data)

# fonction de lecture d'un produit dans le système
@router.get('/{product_id}', response_model=ProductResponseSchema)
async def get_one_product_path(product_id: UUID , db: AsyncSession = Depends(get_db)):
    return await get_one_product(db ,product_id )

# fonction de lecture de tous les produits dans le système
@router.get('/', response_model=ListProductResponseSchema)
async def get_products_path(db: AsyncSession = Depends(get_db)):
    return await get_products(db)

# fonction de modification d'un produit dans le sytème
@router.patch("/{product_id}",response_model=ProductResponseSchema)
async def update_product_path(
    product_id: UUID,
    data: ProductUpdateSchema,
    db: AsyncSession = Depends(get_db)
):
    return await update_product(product_id , data , db)

#route permettant de constituer un produit
@router.post('/constitute-product', response_model = ProductResponseSchema)
async def consttute_new_product_path(data: ConstituateProductSchema, db: AsyncSession = Depends(get_db)):
    
    return await constitute_new_product (db , data)


