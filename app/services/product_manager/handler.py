"""Handlers du module product_manager."""

from uuid import UUID
import uuid

from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status

from app.common.models.Product import Product
from app.common.models.ProductCatalogue import ProductCatalogue
from app.services.product_manager.schemas import ConstituateProductSchema, ListProductResponseSchema, ProductCreateSchema , ProductResponseSchema, ProductUpdateSchema


async def create_product(db: AsyncSession, data: ProductCreateSchema) -> ProductResponseSchema:
    print ('starting function ok✅')
    # casting des clé des conditionnements d'un produit en str
    packagings_id = data.packagings_id
    
    packagings_id = {str(key) : value for key, value in packagings_id.items()}
    
    data.packagings_id = packagings_id
    
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

async def get_one_product(db: AsyncSession , product_id : UUID):
    product_stmt = await db.execute(select(Product).where(and_(Product.id == product_id , Product.deleted_at.is_(None))))
    product = product_stmt.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'Produit non trouvé'
        )
    
    return ProductResponseSchema.model_validate(product)

async def get_products (db: AsyncSession):
    
    product_list_stmt = await db.execute(select(Product).where(Product.deleted_at.is_(None)))
    product_list = product_list_stmt.scalars().all()
    
    try:
        return ListProductResponseSchema(status_code = status.HTTP_200_OK , items = [product_item for product_item in product_list])
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"une erreur s'est produite : {str(exception)}"
        )


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


# fonction permettant de constituer un nouveau produit
async def constitute_new_product (db: AsyncSession , data: ConstituateProductSchema):
    
    product_data = data.model_dump(exclude={'components'})
    
    # transformer les éléments du json des conditionnement en str
    if product_data.get("packagings_id"):
        product_data["packagings_id"] = {str(k): v for k, v in product_data["packagings_id"].items()}
        
    product = Product(**product_data)
    
    try:
        db.add(product)
        await db.flush()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"une erreur est survenue : {str(e)}"
        )
    except Exception as exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"une erreur est survenue : {str(exception)}"
        )
    
    # verification de si les composants du catalogue du produit on été ajouté
    if data.components:
        # construcion d'un tableau pour faire un insert direct
        component_preparation = [
            {
                'id' : uuid.uuid4(),
                'product_id': product.id, # L'ID récupéré grâce au flush()
                'component_id': comp.component_id,
                'quantity': comp.quantity,
                'unit': comp.unit,
            } for comp in data.components
        ]
        
        try:
            # Correction : .values() au pluriel
            stmt = insert(ProductCatalogue).values(component_preparation)
            await db.execute(stmt)
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Erreur sur les composants : {str(e)}")
    
    # 3. Validation finale
    await db.commit()
    await db.refresh(product)
    
    return ProductResponseSchema.model_validate(product)