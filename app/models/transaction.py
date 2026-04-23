from . import get_db_connection

class TransactionModel:
    @staticmethod
    def create(type, amount, category, date, note=""):
        """新增一筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO transactions (type, amount, category, date, note)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (type, amount, category, date, note)
        )
        conn.commit()
        lastrowid = cursor.lastrowid
        conn.close()
        return lastrowid

    @staticmethod
    def get_all():
        """取得所有收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        # 按照日期與建立時間排序，最新的在前面
        cursor.execute('SELECT * FROM transactions ORDER BY date DESC, id DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(transaction_id):
        """根據 ID 取得單筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(transaction_id, type, amount, category, date, note=""):
        """更新單筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE transactions
            SET type = ?, amount = ?, category = ?, date = ?, note = ?
            WHERE id = ?
            ''',
            (type, amount, category, date, note, transaction_id)
        )
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(transaction_id):
        """刪除單筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_summary(month_prefix=None):
        """
        取得收支統計摘要與餘額
        month_prefix: 格式 'YYYY-MM'，如果沒有傳入則計算全部
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = 'SELECT type, SUM(amount) as total FROM transactions'
        params = []
        if month_prefix:
            query += ' WHERE date LIKE ?'
            params.append(f"{month_prefix}%")
        
        query += ' GROUP BY type'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        summary = {'income': 0, 'expense': 0, 'balance': 0}
        for row in rows:
            if row['type'] in summary:
                summary[row['type']] = row['total']
            
        summary['balance'] = summary['income'] - summary['expense']
        return summary
