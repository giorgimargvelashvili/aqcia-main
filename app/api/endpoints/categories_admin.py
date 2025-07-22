from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db.session import SessionLocal
from app.db.models import Category

admin_categories_bp = Blueprint('admin_categories', __name__, template_folder='../../templates/admin')

@admin_categories_bp.route('/admin/categories')
def list_categories():
    db = SessionLocal()
    categories = db.query(Category).all()
    db.close()
    return render_template('admin/categories.html', categories=categories)

@admin_categories_bp.route('/admin/categories/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name_ka = request.form['name_ka']
        name_en = request.form['name_en']
        name_ru = request.form['name_ru']
        icon = request.form.get('icon')

        db = SessionLocal()
        category = Category(name=name_en, name_ka=name_ka, name_en=name_en, name_ru=name_ru, icon=icon)
        db.add(category)
        db.commit()
        db.close()
        flash('Category added successfully!')
        return redirect(url_for('admin_categories.list_categories'))
    return render_template('admin/add_category.html')

@admin_categories_bp.route('/admin/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    db = SessionLocal()
    category = db.query(Category).get(id)
    if request.method == 'POST':
        category.name = request.form['name_en']
        category.name_ka = request.form['name_ka']
        category.name_en = request.form['name_en']
        category.name_ru = request.form['name_ru']
        category.icon = request.form['icon']
        db.commit()
        db.close()
        flash('Category updated successfully!')
        return redirect(url_for('admin_categories.list_categories'))
    db.close()
    return render_template('admin/edit_category.html', category=category)

@admin_categories_bp.route('/admin/categories/delete/<int:id>', methods=['POST'])
def delete_category(id):
    db = SessionLocal()
    category = db.query(Category).get(id)
    db.delete(category)
    db.commit()
    db.close()
    flash('Category deleted successfully!')
    return redirect(url_for('admin_categories.list_categories')) 