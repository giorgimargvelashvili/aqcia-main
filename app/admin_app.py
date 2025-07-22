from flask import Flask
from app.api.endpoints.categories_admin import admin_categories_bp
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

# Register the admin blueprint
app.register_blueprint(admin_categories_bp)

@app.route('/')
def index():
    return '<a href="/admin/categories">Go to Admin Categories Panel</a>'

if __name__ == "__main__":
    app.run(debug=True) 