import sqlite3
from . import get_db_connection

class TransactionModel:
    @staticmethod
    def create(type, amount, category, date, note=""):
        """
        新增一筆收支紀錄
        :param type: 'income' 或 'expense'
        :param amount: 金額 (數字)
        :param category: 分類名稱
        :param date: 發生日期 (YYYY-MM-DD)
        :param note: 備註 (選填)
        :return: 新增的紀錄 ID，若失敗則拋出例外
        """
        try:
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
            return lastrowid
        except sqlite3.Error as e:
            if 'conn' in locals():
                conn.rollback()
            raise e
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有收支紀錄
        :return: 包含所有紀錄的 list of dict
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transactions ORDER BY date DESC, id DESC')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            raise e
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(transaction_id):
        """
        根據 ID 取得單筆收支紀錄
        :param transaction_id: 紀錄的 ID
        :return: 單筆紀錄的 dict，若找不到則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            raise e
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(transaction_id, type, amount, category, date, note=""):
        """
        更新單筆收支紀錄
        :param transaction_id: 要更新的紀錄 ID
        :param type: 'income' 或 'expense'
        :param amount: 金額 (數字)
        :param category: 分類名稱
        :param date: 發生日期 (YYYY-MM-DD)
        :param note: 備註 (選填)
        :return: True 表示成功，若失敗則拋出例外
        """
        try:
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
            return True
        except sqlite3.Error as e:
            if 'conn' in locals():
                conn.rollback()
            raise e
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(transaction_id):
        """
        刪除單筆收支紀錄
        :param transaction_id: 要刪除的紀錄 ID
        :return: True 表示成功，若失敗則拋出例外
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            if 'conn' in locals():
                conn.rollback()
            raise e
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_summary(month_prefix=None):
        """
        取得收支統計摘要與餘額
        :param month_prefix: 格式 'YYYY-MM'，如果沒有傳入則計算全部
        :return: 包含 'income', 'expense', 'balance' 的 dict
        """
        try:
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
            
            summary = {'income': 0, 'expense': 0, 'balance': 0}
            for row in rows:
                if row['type'] in summary:
                    summary[row['type']] = row['total']
                
            summary['balance'] = summary['income'] - summary['expense']
            return summary
        except sqlite3.Error as e:
            raise e
        finally:
            if 'conn' in locals():
                conn.close()
