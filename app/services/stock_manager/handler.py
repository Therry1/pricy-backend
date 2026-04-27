"""Handlers du module stock_manager."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status

from app.common.models.Product import Product
from app.services.stock_manager.schemas import ProductCreateSchema , ProductResponseSchema, ProductUpdateSchema


async def create_product(db: AsyncSession, data: ProductCreateSchema) -> ProductResponseSchema:
    print ('starting function ok✅')
    
    product = Product(**data.model_dump())

    try:
        db.add(product)
        await db.commit()
        await db.refresh(product)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Conflit d'intégrité : {e.orig}",
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur inattendue : {str(e)}",
        )

    return ProductResponseSchema.model_validate(product)

async def update_product(
    product_id: UUID,
    data: ProductUpdateSchema,
    db: AsyncSession
):
    # 🔍 1. Récupérer le produit
    result = await db.execute(
        select(Product).where(
            Product.id == product_id,
            Product.deleted_at == None
        )
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # 🧠 2. Préparer les données
    update_data = data.model_dump(exclude_unset=True, mode="json")

    # 🔄 3. Update dynamique
    for field, value in update_data.items():
        setattr(product, field, value)

    # 💾 4. Sauvegarde
    await db.commit()
    await db.refresh(product)

    # 🎯 5. Retour formaté propre
    return ProductResponseSchema.model_validate(product)