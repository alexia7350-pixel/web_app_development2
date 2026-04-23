from flask import Blueprint, render_template, request
from app.models.transaction import TransactionModel
import datetime

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    """
    處理 GET /
    取得統計摘要與收支明細，並渲染首頁。
    可接受 URL 參數 ?month=YYYY-MM 進行月份篩選。
    """
    month = request.args.get('month')
    if not month:
        # 預設為當月，例如 '2024-05'
        month = datetime.date.today().strftime('%Y-%m')
        
    # 取得當月的統計摘要
    summary = TransactionModel.get_summary(month)
    
    # 取得所有紀錄，並在程式端過濾出符合當月的資料
    all_transactions = TransactionModel.get_all()
    if month:
        transactions = [t for t in all_transactions if t['date'].startswith(month)]
    else:
        transactions = all_transactions
        
    return render_template('index.html', summary=summary, transactions=transactions, current_month=month)
