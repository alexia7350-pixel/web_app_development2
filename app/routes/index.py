from flask import Blueprint, render_template, request

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    """
    處理 GET /
    取得統計摘要與收支明細，並渲染首頁。
    可接受 URL 參數 ?month=YYYY-MM 進行月份篩選。
    """
    pass
