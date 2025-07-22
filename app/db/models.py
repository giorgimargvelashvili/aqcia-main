from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, DECIMAL, JSON, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base, backref

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    location = Column(String(255))
    location_permission_granted = Column(Boolean)
    notification_preferences = Column(String(255))
    created_at = Column(DateTime)
    sessions = relationship('Session', back_populates='user')
    preferences = relationship('Preference', back_populates='user', uselist=False)
    search_history = relationship('SearchHistory', back_populates='user')
    shopping_lists = relationship('ShoppingList', back_populates='user')
    favorites = relationship('Favorite', back_populates='user')
    sale_alerts = relationship('SaleAlert', back_populates='user')
    notifications = relationship('Notification', back_populates='user')

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    is_guest = Column(Boolean)
    is_first_time = Column(Boolean)
    started_at = Column(DateTime)
    last_active = Column(DateTime)
    user = relationship('User', back_populates='sessions')

class Preference(Base):
    __tablename__ = 'preferences'
    preference_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    dietary_filters = Column(String(255))
    favorite_stores = Column(Text)
    saved_searches = Column(Text)
    route_suggestions = Column(Boolean, default=True)
    user = relationship('User', back_populates='preferences')

class SearchHistory(Base):
    __tablename__ = 'search_history'
    search_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    query = Column(Text)
    searched_at = Column(DateTime)
    user = relationship('User', back_populates='search_history')

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    api_product_id = Column(Integer, unique=True, index=True, nullable=True)
    name = Column(String(255), index=True)
    brand = Column(String(255), nullable=True)
    bar_code = Column(String(255), nullable=True)
    image_url = Column(String(512), nullable=True)
    
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'))
    subcategory = relationship('Subcategory', back_populates='products')

    # --- Relationships ---
    smart_matches = relationship('SmartMatching', back_populates='product')
    inventory = relationship('Inventory', back_populates='product')
    prices = relationship('Price', back_populates='product')
    price_history = relationship('PriceHistory', back_populates='product')
    shopping_list_items = relationship('ShoppingListItem', back_populates='product')
    favorites = relationship('Favorite', back_populates='product')
    sale_alerts = relationship('SaleAlert', back_populates='product')
    notifications = relationship('Notification', back_populates='product')

class SmartMatching(Base):
    __tablename__ = 'smart_matching'
    match_id = Column(Integer, primary_key=True, autoincrement=True)
    input_query = Column(String(255))
    matched_product_id = Column(Integer, ForeignKey('products.product_id'))
    confidence_score = Column(Float)
    synonym_used = Column(String(255))
    variation_type = Column(String(255))
    product = relationship('Product', back_populates='smart_matches')

class Store(Base):
    __tablename__ = 'stores'
    store_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    location = Column(String(255))
    latitude = Column(DECIMAL(9,6), nullable=True)
    longitude = Column(DECIMAL(9,6), nullable=True)
    chain_id = Column(Integer, nullable=True)
    api_source = Column(String(255))
    is_active = Column(Boolean, default=True)
    inventory = relationship('Inventory', back_populates='store')
    prices = relationship('Price', back_populates='store')
    price_history = relationship('PriceHistory', back_populates='store')
    notifications = relationship('Notification', back_populates='store')

class Inventory(Base):
    __tablename__ = 'inventory'
    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('stores.store_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer)
    last_restocked = Column(DateTime, nullable=True)
    updated_at = Column(DateTime)
    store = relationship('Store', back_populates='inventory')
    product = relationship('Product', back_populates='inventory')

class Price(Base):
    __tablename__ = 'prices'
    price_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('stores.store_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    price = Column(DECIMAL(10,2))
    sale_price = Column(DECIMAL(10,2), nullable=True)
    is_on_sale = Column(Boolean, default=False)
    sale_start = Column(DateTime, nullable=True)
    sale_end = Column(DateTime, nullable=True)
    updated_at = Column(DateTime)
    store = relationship('Store', back_populates='prices')
    product = relationship('Product', back_populates='prices')

class PriceHistory(Base):
    __tablename__ = 'price_history'
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('stores.store_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    price = Column(DECIMAL(10,2))
    was_on_sale = Column(Boolean, default=False)
    sale_price = Column(DECIMAL(10,2), nullable=True)
    recorded_at = Column(DateTime)
    store = relationship('Store', back_populates='price_history')
    product = relationship('Product', back_populates='price_history')

class ShoppingList(Base):
    __tablename__ = 'shopping_lists'
    list_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(255))
    created_at = Column(DateTime)
    last_updated = Column(DateTime)
    user = relationship('User', back_populates='shopping_lists')
    items = relationship('ShoppingListItem', back_populates='shopping_list')

class ShoppingListItem(Base):
    __tablename__ = 'shopping_list_items'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    list_id = Column(Integer, ForeignKey('shopping_lists.list_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer, default=1)
    added_at = Column(DateTime)
    shopping_list = relationship('ShoppingList', back_populates='items')
    product = relationship('Product', back_populates='shopping_list_items')

class Favorite(Base):
    __tablename__ = 'favorites'
    favorite_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    added_at = Column(DateTime)
    notify_on_sale = Column(Boolean, default=False)
    user = relationship('User', back_populates='favorites')
    product = relationship('Product', back_populates='favorites')

class SaleAlert(Base):
    __tablename__ = 'sale_alerts'
    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    notify_on_sale = Column(Boolean, default=True)
    notify_if_already_on_sale = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    last_notified = Column(DateTime, nullable=True)
    user = relationship('User', back_populates='sale_alerts')
    product = relationship('Product', back_populates='sale_alerts')

class Notification(Base):
    __tablename__ = 'notifications'
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    store_id = Column(Integer, ForeignKey('stores.store_id'), nullable=True)
    type = Column(String(255))
    message = Column(Text)
    sent_at = Column(DateTime)
    is_read = Column(Boolean, default=False)
    extra_metadata = Column(JSON, nullable=True)
    user = relationship('User', back_populates='notifications')
    product = relationship('Product', back_populates='notifications')
    store = relationship('Store', back_populates='notifications')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_ka = Column(String(255), nullable=True)
    name_en = Column(String(255), nullable=True)
    name_ru = Column(String(255), nullable=True)
    icon = Column(String(255), nullable=True)
    api_category_id = Column(Integer, unique=True, index=True)

    # Removed: parent_id, subcategories, products relationships
    # Only top-level categories remain

    __table_args__ = (
        UniqueConstraint('name', name='_category_name_uc'),
    )

class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_ka = Column(String(255), nullable=True)
    name_en = Column(String(255), nullable=True)
    name_ru = Column(String(255), nullable=True)
    icon = Column(String(255), nullable=True)
    api_subcategory_id = Column(Integer, unique=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', backref=backref('subcategories', cascade='all, delete-orphan'))
    products = relationship('Product', back_populates='subcategory')

    __table_args__ = (
        UniqueConstraint('category_id', 'name', name='_category_subcategory_uc'),
    )
