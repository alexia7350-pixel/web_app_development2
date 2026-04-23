# 路由與頁面設計 (ROUTES) - 個人記帳簿系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁與月度報表總覽 | GET | `/` | `templates/index.html` | 顯示當月總收支、餘額與歷史明細 |
| 新增收支頁面 | GET | `/transactions/new` | `templates/transactions/new.html` | 顯示填寫收支紀錄的表單 |
| 建立收支紀錄 | POST | `/transactions` | — | 接收表單，存入 DB，重導向至首頁 |
| 修改收支頁面 | GET | `/transactions/<id>/edit` | `templates/transactions/edit.html` | 顯示修改單筆紀錄的表單 |
| 更新收支紀錄 | POST | `/transactions/<id>/update` | — | 接收表單，更新 DB，重導向至首頁 |
| 刪除收支紀錄 | POST | `/transactions/<id>/delete` | — | 刪除指定紀錄，重導向至首頁 |

## 2. 每個路由的詳細說明

### `GET /` (首頁)
- **輸入**：可選的 URL 參數 `month` (例如 `?month=2024-05`)
- **處理邏輯**：呼叫 `TransactionModel.get_summary(month)` 計算當月餘額，並呼叫 `TransactionModel.get_all()` (搭配條件) 取得列表。
- **輸出**：渲染 `index.html`
- **錯誤處理**：無特定錯誤，若無資料則顯示空狀態。

### `GET /transactions/new` (新增收支頁面)
- **輸入**：無
- **處理邏輯**：單純回傳表單頁面。
- **輸出**：渲染 `transactions/new.html`

### `POST /transactions` (建立收支紀錄)
- **輸入**：表單欄位 `type`, `amount`, `category`, `date`, `note`
- **處理邏輯**：驗證欄位是否為空、amount 是否為數字。成功則呼叫 `TransactionModel.create(...)`。
- **輸出**：成功後 HTTP 302 重導向至 `/`。
- **錯誤處理**：驗證失敗時，渲染 `transactions/new.html` 並顯示錯誤訊息。

### `GET /transactions/<id>/edit` (修改收支頁面)
- **輸入**：URL 變數 `id`
- **處理邏輯**：呼叫 `TransactionModel.get_by_id(id)`，若找不到回傳 404。
- **輸出**：渲染 `transactions/edit.html`，並預填舊資料。
- **錯誤處理**：若 ID 不存在，回傳 404 Not Found 或重導向回首頁並顯示錯誤。

### `POST /transactions/<id>/update` (更新收支紀錄)
- **輸入**：URL 變數 `id`，表單欄位 `type`, `amount`, `category`, `date`, `note`
- **處理邏輯**：驗證欄位。成功則呼叫 `TransactionModel.update(...)`。
- **輸出**：成功後 HTTP 302 重導向至 `/`。
- **錯誤處理**：驗證失敗時，渲染 `transactions/edit.html` 並顯示錯誤。

### `POST /transactions/<id>/delete` (刪除收支紀錄)
- **輸入**：URL 變數 `id`
- **處理邏輯**：呼叫 `TransactionModel.delete(id)`。
- **輸出**：成功後 HTTP 302 重導向至 `/`。

## 3. Jinja2 模板清單

1. `templates/base.html`：所有頁面的共用基底模板（包含 Header、Footer、CSS 引入等共同元素）。
2. `templates/index.html`：繼承自 `base.html`，顯示統計摘要與收支列表。
3. `templates/transactions/new.html`：繼承自 `base.html`，新增收支的表單。
4. `templates/transactions/edit.html`：繼承自 `base.html`，修改收支的表單。

## 4. 路由骨架程式碼
骨架程式碼已建立於 `app/routes/` 目錄中，並採用 Flask Blueprint 進行模組化管理：
- `app/routes/index.py` (首頁路由)
- `app/routes/transaction.py` (收支紀錄相關路由)
