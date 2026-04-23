# 流程圖設計 (FLOWCHART) - 個人記帳簿系統

## 1. 使用者流程圖（User Flow）
此流程圖描述使用者進入記帳系統後，可以進行的各項操作路徑。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 總覽與月度報表]
    B --> C{要執行什麼操作？}
    
    C -->|新增收支| D[點擊新增按鈕]
    D --> E[填寫收支表單\n金額、分類、備註]
    E --> F{提交表單}
    F -->|成功| B
    F -->|失敗/資料不完整| E
    
    C -->|查看紀錄| G[點擊歷史紀錄]
    G --> H[顯示收支明細列表]
    
    H --> I{對單筆紀錄操作？}
    I -->|修改紀錄| J[進入修改表單]
    J --> K{儲存變更}
    K -->|成功| H
    K -->|失敗| J
    
    I -->|刪除紀錄| L{確認刪除？}
    L -->|確認| H
    L -->|取消| H
    
    I -->|返回首頁| B
```

## 2. 系統序列圖（Sequence Diagram）
以「使用者新增一筆收支紀錄」為例，展示前端瀏覽器、Flask 後端與 SQLite 資料庫的完整資料流互動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask (Route & Model)
    participant DB as SQLite 資料庫

    User->>Browser: 在首頁點擊「新增」
    Browser->>Flask: GET /transaction/add
    Flask-->>Browser: 回傳新增表單 HTML
    
    User->>Browser: 填寫金額、分類等資訊並送出
    Browser->>Flask: POST /transaction/add (包含表單資料)
    
    Note over Flask: 驗證資料格式 (如：金額是否為數字)
    
    alt 資料驗證失敗
        Flask-->>Browser: 回傳錯誤訊息與原表單 HTML
        Browser-->>User: 顯示錯誤提示
    else 資料驗證成功
        Flask->>DB: INSERT INTO transactions (新增資料)
        DB-->>Flask: 寫入成功
        Flask-->>Browser: HTTP 302 重新導向至首頁 (GET /)
        Browser->>Flask: GET /
        Flask->>DB: 查詢最新當月收支總和與明細
        DB-->>Flask: 回傳查詢結果
        Flask-->>Browser: 渲染包含最新數據的首頁 HTML
        Browser-->>User: 看到更新後的餘額與剛新增的紀錄
    end
```

## 3. 功能清單對照表
此表對應了 PRD 中定義的核心功能，與接下來即將實作的 URL 路由規劃。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| 首頁與月度報表總覽 | `/` | GET | 顯示當月總收入、總支出、餘額與統計圖表 |
| 進入新增收支頁面 | `/transaction/add` | GET | 顯示填寫收支紀錄的表單頁面 |
| 處理新增收支請求 | `/transaction/add` | POST | 接收表單資料並存入資料庫，成功後回首頁 |
| 歷史紀錄明細查詢 | `/history` | GET | 顯示所有過去的收支明細列表 |
| 進入修改收支頁面 | `/transaction/edit/<id>` | GET | 根據紀錄 ID 顯示預填舊資料的修改表單 |
| 處理修改收支請求 | `/transaction/edit/<id>` | POST | 更新資料庫中特定 ID 的紀錄，成功後回歷史列表 |
| 處理刪除收支請求 | `/transaction/delete/<id>` | POST | 刪除資料庫中特定 ID 的紀錄，成功後回歷史列表 |
