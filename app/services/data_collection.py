from sqlalchemy.orm import Session
from app.db.session import engine
from app.db import models
from datetime import datetime

def process_scraped_data(data):
    with engine.begin() as conn:
        session = Session(bind=conn)
        for item in data:
            # Upsert product
            product = session.query(models.Product).filter_by(
                name=item.name, brand=item.brand, size=item.size
            ).first()
            if not product:
                product = models.Product(
                    name=item.name,
                    brand=item.brand,
                    type=getattr(item, 'type', None),
                    size=item.size,
                    upc=getattr(item, 'upc', None),
                    keywords=getattr(item, 'keywords', None),
                )
                session.add(product)
                session.flush()  # get product_id
            # Upsert store
            store = session.query(models.Store).filter_by(
                name=item.store_name, location=item.store_location
            ).first()
            if not store:
                store = models.Store(
                    name=item.store_name,
                    location=item.store_location,
                    api_source=getattr(item, 'api_source', None),
                )
                session.add(store)
                session.flush()  # get store_id
            # Upsert inventory
            inventory = session.query(models.Inventory).filter_by(
                store_id=store.store_id, product_id=product.product_id
            ).first()
            now = datetime.utcnow()
            if not inventory:
                inventory = models.Inventory(
                    store_id=store.store_id,
                    product_id=product.product_id,
                    quantity=getattr(item, 'quantity', 0),
                    last_restocked=getattr(item, 'last_restocked', None),
                    updated_at=now,
                )
                session.add(inventory)
            else:
                inventory.quantity = getattr(item, 'quantity', inventory.quantity)
                inventory.last_restocked = getattr(item, 'last_restocked', inventory.last_restocked)
                inventory.updated_at = now
            # Upsert price
            price = session.query(models.Price).filter_by(
                store_id=store.store_id, product_id=product.product_id
            ).first()
            if not price:
                price = models.Price(
                    store_id=store.store_id,
                    product_id=product.product_id,
                    price=item.price,
                    sale_price=getattr(item, 'sale_price', None),
                    is_on_sale=getattr(item, 'is_on_sale', False),
                    sale_start=getattr(item, 'sale_start', None),
                    sale_end=getattr(item, 'sale_end', None),
                    updated_at=now,
                )
                session.add(price)
            else:
                price.price = item.price
                price.sale_price = getattr(item, 'sale_price', price.sale_price)
                price.is_on_sale = getattr(item, 'is_on_sale', price.is_on_sale)
                price.sale_start = getattr(item, 'sale_start', price.sale_start)
                price.sale_end = getattr(item, 'sale_end', price.sale_end)
                price.updated_at = now
        session.commit()
