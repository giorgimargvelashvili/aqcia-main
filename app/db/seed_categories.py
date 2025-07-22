import os
import re
import ast
from app.db.session import SessionLocal
from app.db.models import Category

MOCK_FILE = os.path.join(os.path.dirname(__file__), '../../products-mocks.ts.txt')

def parse_categories():
    with open(MOCK_FILE, encoding='utf-8') as f:
        content = f.read()
    # Find the categories array
    match = re.search(r'categories:\s*\[(.*?)\],\s*products:', content, re.DOTALL)
    if not match:
        print('No categories found!')
        return []
    categories_str = match.group(1)
    # Replace JS-style keys with Python keys
    categories_str = re.sub(r'(\w+):', r'"\1":', categories_str)
    # Replace single quotes with double quotes
    categories_str = categories_str.replace("'", '"')
    # Convert to list
    try:
        categories = ast.literal_eval(f'[{categories_str}]')
    except Exception as e:
        print('Error parsing categories:', e)
        return []
    return categories

def seed_categories():
    db = SessionLocal()
    categories = parse_categories()
    for cat in categories:
        exists = db.query(Category).filter_by(name=cat['id']).first()
        if not exists:
            db.add(Category(
                name=cat['id'],
                name_ka=cat['name'][0],
                name_en=cat['name'][1],
                name_ru=cat['name'][2],
                icon=cat.get('icon', None)
            ))
    db.commit()
    db.close()
    print(f'Seeded {len(categories)} categories.')

if __name__ == '__main__':
    seed_categories() 