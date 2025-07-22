import requests
import time
from datetime import datetime
from decimal import Decimal, InvalidOperation
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Product, Price, Store, Category, Subcategory
import traceback

BASE_URL = "https://api.agrohub.ge/v1/Products/GetGroupedProducts"
CATEGORIES_URL = "https://api.agrohub.ge/v1/Categories?ShopId=1"
SUBCATEGORIES_URL = "https://api.agrohub.ge/v1/Categories/subcategories?categoryId={categoryId}&shopId=1"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkZBNjEwNzA1NDFDODNFQjNFMTQzODVDODA1Q0MwNjcyNEY1RjkyMjYiLCJ0eXAiOiJKV1QiLCJ4NXQiOiItbUVIQlVISVByUGhRNFhJQmN3R2NrOWZraVkifQ.eyJuYmYiOjE3NTMwODg1MzYsImV4cCI6MjA2ODQ0ODUzNiwiaXNzIjoiaHR0cHM6Ly9hcGkuYWdyb2h1Yi5nZS8iLCJhdWQiOlsiaHR0cHM6Ly9hcGkuYWdyb2h1Yi5nZS9yZXNvdXJjZXMiLCJBcGkiXSwiY2xpZW50X2lkIjoiR3JvY2VyeVdlYiIsInNjb3BlIjpbIkdyb2NlcnlBcGkiXX0.YqYNJJM96IUUGjjZRihFv0BW5LoKZuuYDKc3hQzaMTjM0wKLtfCI_NW-qoxXM9qYExvjk6FTP1qmu1R50imY6UrwkAbqkoZAvjTkvPk3CdBR9Gcem6aoVz6mem6KKlXAK8ec5CPxFc9xi_m-Ifr94-m5-jLJH-iZTomhBZiS4daLnDCMOiSBgVSLjhm57DsafZPDv-vJsMuwYYd7QB_cFsbpqcqe4svqZen92GKLiaM4msIGqzjht_KvlW1IerbNvc90mXjLucz8fMdyKpQ-ZTQyN6-p73GxXPkQE5c-m3zX-eqdmIDjdyhauo0MGjcdIHL9hSmoswfS4omjiKWq-w"
}


def fetch_categories():
    resp = requests.get(CATEGORIES_URL, headers=HEADERS)
    resp.raise_for_status()
    return resp.json().get("categories", [])

def fetch_subcategories(category_id):
    url = SUBCATEGORIES_URL.format(categoryId=category_id)
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    # If the response is a list, just return it
    if isinstance(data, list):
        return data
    # If it's a dict, return the subCategories key if present
    return data.get("subCategories", [])

def fetch_products_from_api(parent_category_id, subcategory_id=None, page_number=1, page_size=50):
    params = {
        "ShopId": 1,
        "ParentCategoryId": parent_category_id,
        "PageNumber": page_number,
        "PageSize": page_size,
    }
    if subcategory_id:
        params["SubCategoryId"] = subcategory_id
    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Error fetching products for parent {parent_category_id}, subcategory {subcategory_id}: {e}")
        return None

def parse_and_save_products(db: Session, store_id: int, api_data: dict, parent_category_db: Category, subcategory_db: Subcategory):
    try:
        if not isinstance(api_data, dict):
            print(f"Error: api_data is not a dict, got {type(api_data)}. Value: {str(api_data)[:500]}")
            return 0
        if 'groupedProduct' not in api_data:
            print("Error: 'groupedProduct' not in api_data. Keys: {}".format(list(api_data.keys())))
            return 0
        product_count = 0
        grouped_products = api_data['groupedProduct']
        print(f"grouped_products type: {type(grouped_products)}, value: {str(grouped_products)[:500]}")
        if not isinstance(grouped_products, list):
            print(f"Warning: groupedProduct is not a list: {type(grouped_products)}")
            return 0
        for group in grouped_products:
            print(f"group type: {type(group)}, value: {str(group)[:500]}")
            products = group['products'] if isinstance(group, dict) and 'products' in group else []
            print(f"products type: {type(products)}, value: {str(products)[:500]}")
            if not isinstance(products, list):
                print(f"Warning: products is not a list in group: {group}")
                continue
            for p_data in products:
                product_count += 1
                product = db.query(Product).filter(Product.api_product_id == p_data['id']).first()
                if not product:
                    product = Product(
                        api_product_id=p_data['id'],
                        name=p_data.get('name'),
                        bar_code=p_data.get('barCode'),
                        image_url=p_data.get('imageUrl'),
                        subcategory_id=subcategory_db.id
                    )
                    db.add(product)
                    db.flush()
                else:
                    product.subcategory_id = subcategory_db.id
                price = db.query(Price).filter(Price.product_id == product.product_id, Price.store_id == store_id).first()
                if not price:
                    price = Price(store_id=store_id, product_id=product.product_id)
                    db.add(price)
                price.price = Decimal(p_data['price']) if p_data.get('price') else None
                price.sale_price = Decimal(p_data['previousPrice']) if p_data.get('previousPrice') else None
                price.is_on_sale = bool(p_data.get('previousPrice'))
                price.updated_at = datetime.utcnow()
        db.commit()
        return product_count
    except Exception as e:
        print("Exception in parse_and_save_products:")
        traceback.print_exc()
        print(f"api_data type: {type(api_data)}, value: {str(api_data)[:500]}")
        return 0

def run_scrape():
    print(f"\n[{datetime.now()}] Starting Agrohub scrape...")
    db: Session = SessionLocal()
    try:
        try:
            store = db.query(Store).filter(Store.name == "Agrohub").first()
            if not store:
                store = Store(name="Agrohub", api_source="https://agrohub.ge", is_active=True)
                db.add(store)
                db.commit()

            categories = fetch_categories()
            print(f"categories type: {type(categories)}, value: {str(categories)[:500]}")
            for cat in categories:
                print(f"cat type: {type(cat)}, value: {str(cat)[:500]}")
                parent_category_db = db.query(Category).filter(Category.api_category_id == cat["id"]).first()
                if not parent_category_db:
                    parent_category_db = Category(
                        name=cat["name"],
                        name_ka=cat["name"],
                        name_en=cat["name"],
                        name_ru=cat["name"],
                        api_category_id=cat["id"]
                    )
                    db.add(parent_category_db)
                    db.commit()
                subcategories = fetch_subcategories(cat["id"])
                print(f"subcategories type: {type(subcategories)}, value: {str(subcategories)[:500]}")
                for subcat in subcategories:
                    print(f"subcat type: {type(subcat)}, value: {str(subcat)[:500]}")
                    subcategory_db = db.query(Subcategory).filter_by(
                        api_subcategory_id=subcat["id"],
                        category_id=parent_category_db.id
                    ).first()
                    if not subcategory_db:
                        subcategory_db = Subcategory(
                            name=subcat["name"],
                            api_subcategory_id=subcat["id"],
                            category_id=parent_category_db.id
                        )
                        db.add(subcategory_db)
                        db.commit()
                    page = 1
                    while True:
                        try:
                            print(f"[{datetime.now()}] Fetching page {page} for category {cat['id']} subcategory {subcat['id']}...")
                            api_data = fetch_products_from_api(cat["id"], subcat["id"], page_number=page)
                            if not api_data:
                                break
                            print(f"api_data type: {type(api_data)}, value: {str(api_data)[:500]}")
                            parse_and_save_products(db, store.store_id, api_data, parent_category_db, subcategory_db)
                            # Only call .get if api_data is a dict
                            if isinstance(api_data, dict):
                                if api_data.get('hasNextPage'):
                                    page += 1
                                    time.sleep(1)
                                else:
                                    break
                            else:
                                break
                        except Exception as e:
                            print("Exception in main scraping loop:")
                            traceback.print_exc()
                            print(f"api_data type: {type(api_data)}, value: {str(api_data)[:500]}")
                            break
            print(f"[{datetime.now()}] Scrape complete.")
        except Exception as e:
            print("Exception in run_scrape global try/except:")
            traceback.print_exc()
    except Exception as e:
        print(f"[{datetime.now()}] AN ERROR OCCURRED: {e}")
        db.rollback()
    finally:
        db.close() 