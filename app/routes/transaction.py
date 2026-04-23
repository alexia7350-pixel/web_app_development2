from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@bp.route('/new', methods=['GET'])
def new_transaction():
    """
    處理 GET /transactions/new
    顯示新增收支的表單頁面。
    """
    pass

@bp.route('', methods=['POST'])
def create_transaction():
    """
    處理 POST /transactions
    接收表單資料，驗證後寫入資料庫。
    成功則重導向回首頁；失敗則重新渲染新增表單並顯示錯誤。
    """
    pass

@bp.route('/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    """
    處理 GET /transactions/<id>/edit
    根據 ID 取得單筆收支紀錄，並顯示於修改表單中供使用者編輯。
    """
    pass

@bp.route('/<int:id>/update', methods=['POST'])
def update_transaction(id):
    """
    處理 POST /transactions/<id>/update
    接收表單資料，驗證後更新資料庫中對應 ID 的紀錄。
    成功則重導向回首頁；失敗則重新渲染修改表單並顯示錯誤。
    """
    pass

@bp.route('/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    處理 POST /transactions/<id>/delete
    刪除資料庫中對應 ID 的紀錄。
    成功後重導向回首頁。
    """
    pass
