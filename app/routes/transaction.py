from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.transaction import TransactionModel

bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@bp.route('/new', methods=['GET'])
def new_transaction():
    """
    處理 GET /transactions/new
    顯示新增收支的表單頁面。
    """
    return render_template('transactions/new.html', form_data={})

@bp.route('', methods=['POST'])
def create_transaction():
    """
    處理 POST /transactions
    接收表單資料，驗證後寫入資料庫。
    成功則重導向回首頁；失敗則重新渲染新增表單並顯示錯誤。
    """
    type = request.form.get('type')
    amount = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('date')
    note = request.form.get('note', '')

    if not all([type, amount, category, date]):
        flash('請填寫所有必填欄位！', 'danger')
        return render_template('transactions/new.html', form_data=request.form)
        
    try:
        amount = float(amount)
        if type not in ['income', 'expense']:
            raise ValueError("Type 必須是 'income' 或 'expense'")
    except ValueError:
        flash('輸入資料格式錯誤！金額必須是數字。', 'danger')
        return render_template('transactions/new.html', form_data=request.form)

    try:
        TransactionModel.create(type, amount, category, date, note)
        flash('成功新增一筆紀錄！', 'success')
        return redirect(url_for('index.index'))
    except Exception as e:
        flash(f'資料庫發生錯誤：{str(e)}', 'danger')
        return render_template('transactions/new.html', form_data=request.form)

@bp.route('/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    """
    處理 GET /transactions/<id>/edit
    根據 ID 取得單筆收支紀錄，並顯示於修改表單中供使用者編輯。
    """
    transaction = TransactionModel.get_by_id(id)
    if not transaction:
        flash('找不到該筆紀錄！', 'danger')
        return redirect(url_for('index.index'))
        
    return render_template('transactions/edit.html', transaction=transaction)

@bp.route('/<int:id>/update', methods=['POST'])
def update_transaction(id):
    """
    處理 POST /transactions/<id>/update
    接收表單資料，驗證後更新資料庫中對應 ID 的紀錄。
    成功則重導向回首頁；失敗則重新渲染修改表單並顯示錯誤。
    """
    type = request.form.get('type')
    amount = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('date')
    note = request.form.get('note', '')

    if not all([type, amount, category, date]):
        flash('請填寫所有必填欄位！', 'danger')
        # 合併原本的 id 讓模板依然能渲染正確的 url
        form_data = {'id': id, **request.form}
        return render_template('transactions/edit.html', transaction=form_data)
        
    try:
        amount = float(amount)
        if type not in ['income', 'expense']:
            raise ValueError("Type 必須是 'income' 或 'expense'")
    except ValueError:
        flash('輸入資料格式錯誤！金額必須是數字。', 'danger')
        form_data = {'id': id, **request.form}
        return render_template('transactions/edit.html', transaction=form_data)

    try:
        TransactionModel.update(id, type, amount, category, date, note)
        flash('紀錄更新成功！', 'success')
        return redirect(url_for('index.index'))
    except Exception as e:
        flash(f'資料庫發生錯誤：{str(e)}', 'danger')
        form_data = {'id': id, **request.form}
        return render_template('transactions/edit.html', transaction=form_data)

@bp.route('/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    處理 POST /transactions/<id>/delete
    刪除資料庫中對應 ID 的紀錄。
    成功後重導向回首頁。
    """
    try:
        TransactionModel.delete(id)
        flash('紀錄已成功刪除！', 'success')
    except Exception as e:
        flash(f'刪除失敗：{str(e)}', 'danger')
        
    return redirect(url_for('index.index'))
