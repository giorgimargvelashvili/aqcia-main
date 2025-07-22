from fastapi import FastAPI
from app.api.endpoints import products, prices, inventory, users, shopping_lists, favorites, sale_alerts, notifications, search, data_collection_router
from sqladmin import Admin, ModelView
from app.db.session import engine
from app.db import models
from fastapi import Depends, Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.api.endpoints.categories_admin import admin_categories_bp
from flask import Flask

app = FastAPI() if 'FastAPI' in globals() else Flask(__name__)

# Include routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(prices.router, prefix="/prices", tags=["Prices"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(shopping_lists.router, prefix="/shopping-lists", tags=["Shopping Lists"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(sale_alerts.router, prefix="/sale-alerts", tags=["Sale Alerts"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(data_collection_router, prefix="/data-collection", tags=["Data Collection"])
# app.register_blueprint(admin_categories_bp)

# --- SQLAdmin setup ---

# Register all models with SQLAdmin
class UserAdmin(ModelView, model=models.User):
    column_list = [c.name for c in models.User.__table__.columns]
class SessionAdmin(ModelView, model=models.Session):
    column_list = [c.name for c in models.Session.__table__.columns]
class PreferenceAdmin(ModelView, model=models.Preference):
    column_list = [c.name for c in models.Preference.__table__.columns]
class SearchHistoryAdmin(ModelView, model=models.SearchHistory):
    column_list = [c.name for c in models.SearchHistory.__table__.columns]
class ProductAdmin(ModelView, model=models.Product):
    column_list = [c.name for c in models.Product.__table__.columns]
class SmartMatchingAdmin(ModelView, model=models.SmartMatching):
    column_list = [c.name for c in models.SmartMatching.__table__.columns]
class StoreAdmin(ModelView, model=models.Store):
    column_list = [c.name for c in models.Store.__table__.columns]
class InventoryAdmin(ModelView, model=models.Inventory):
    column_list = [c.name for c in models.Inventory.__table__.columns]
class PriceAdmin(ModelView, model=models.Price):
    column_list = [c.name for c in models.Price.__table__.columns]
class PriceHistoryAdmin(ModelView, model=models.PriceHistory):
    column_list = [c.name for c in models.PriceHistory.__table__.columns]
class ShoppingListAdmin(ModelView, model=models.ShoppingList):
    column_list = [c.name for c in models.ShoppingList.__table__.columns]
class ShoppingListItemAdmin(ModelView, model=models.ShoppingListItem):
    column_list = [c.name for c in models.ShoppingListItem.__table__.columns]
class FavoriteAdmin(ModelView, model=models.Favorite):
    column_list = [c.name for c in models.Favorite.__table__.columns]
class SaleAlertAdmin(ModelView, model=models.SaleAlert):
    column_list = [c.name for c in models.SaleAlert.__table__.columns]
class NotificationAdmin(ModelView, model=models.Notification):
    column_list = [c.name for c in models.Notification.__table__.columns]

admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(SessionAdmin)
admin.add_view(PreferenceAdmin)
admin.add_view(SearchHistoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(SmartMatchingAdmin)
admin.add_view(StoreAdmin)
admin.add_view(InventoryAdmin)
admin.add_view(PriceAdmin)
admin.add_view(PriceHistoryAdmin)
admin.add_view(ShoppingListAdmin)
admin.add_view(ShoppingListItemAdmin)
admin.add_view(FavoriteAdmin)
admin.add_view(SaleAlertAdmin)
admin.add_view(NotificationAdmin)
# --- End SQLAdmin setup ---

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Price Comparison API is running!"}
  
  
if __name__ == "__main__":
    app.run(debug=True)