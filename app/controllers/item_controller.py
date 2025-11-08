"""
Item controller for CRUD operations
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Item

bp = Blueprint('items', __name__, url_prefix='/items')


@bp.route('/')
def list_items():
    """List all items"""
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('items/list.html', items=items)


@bp.route('/create', methods=['GET', 'POST'])
def create_item():
    """Create a new item"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        style = request.form.get('style')
        
        if not name:
            flash('الاسم مطلوب / Name is required', 'error')
            return render_template('items/create.html')
        
        item = Item(name=name, description=description, style=style)
        db.session.add(item)
        db.session.commit()
        
        flash('تم إضافة العنصر بنجاح / Item added successfully', 'success')
        return redirect(url_for('items.list_items'))
    
    return render_template('items/create.html')


@bp.route('/<int:item_id>')
def view_item(item_id):
    """View a single item"""
    item = Item.query.get_or_404(item_id)
    return render_template('items/view.html', item=item)


@bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    """Edit an existing item"""
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.style = request.form.get('style')
        
        if not item.name:
            flash('الاسم مطلوب / Name is required', 'error')
            return render_template('items/edit.html', item=item)
        
        db.session.commit()
        flash('تم تحديث العنصر بنجاح / Item updated successfully', 'success')
        return redirect(url_for('items.view_item', item_id=item.id))
    
    return render_template('items/edit.html', item=item)


@bp.route('/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    """Delete an item"""
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    flash('تم حذف العنصر بنجاح / Item deleted successfully', 'success')
    return redirect(url_for('items.list_items'))
