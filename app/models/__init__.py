import sqlite3
import os

def get_db_connection():
    """取得 SQLite 資料庫連線"""
    # 取得 instance 目錄的路徑 (與 app 同層)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    instance_dir = os.path.join(base_dir, 'instance')
    
    # 確保 instance 資料夾存在
    os.makedirs(instance_dir, exist_ok=True)
    
    db_path = os.path.join(instance_dir, 'database.db')
    conn = sqlite3.connect(db_path)
    
    # 設定 row_factory 使查詢結果可用字典方式存取欄位
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫與資料表"""
    conn = get_db_connection()
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    schema_path = os.path.join(base_dir, 'database', 'schema.sql')
    
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
            
    conn.commit()
    conn.close()
