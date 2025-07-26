# 案件管理系統

這是一個基於 Django 的案件管理系統，提供完整的 CRUD 功能、用戶認證、搜尋篩選和分頁功能。

## 功能特色

- ✅ **用戶認證系統** (使用 django-allauth)
- ✅ **完整的 CRUD 操作** (建立、讀取、更新、刪除案件)
- ✅ **模糊搜尋** (支援案號、地址、負責人等欄位搜尋)
- ✅ **多條件篩選** (狀態、縣市、鄉鎮區里)
- ✅ **排序功能** (多種排序選項)
- ✅ **分頁顯示** (每頁 10 筆資料)
- ✅ **響應式設計** (使用 Bootstrap 5)
- ✅ **權限控制** (只有案件負責人或管理員可編輯)

## 技術架構

- **後端框架**: Django 5.2.4
- **認證系統**: django-allauth
- **前端框架**: Bootstrap 5
- **資料庫**: SQLite (開發環境)
- **圖示**: Font Awesome 6

## 安裝與設定

### 1. 克隆專案

```bash
git clone <repository-url>
cd case_management
```

### 2. 建立虛擬環境

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# 或
source venv/bin/activate      # Linux/Mac
```

### 3. 安裝依賴

```bash
pip install django django-allauth
```

### 4. 資料庫遷移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 建立超級用戶

```bash
python manage.py createsuperuser
```

### 6. 建立測試資料

```bash
python create_test_data.py
```

### 7. 啟動開發伺服器

```bash
python manage.py runserver
```

## 使用說明

### 登入系統

1. 訪問 http://localhost:8000
2. 點擊右上角「登入」
3. 使用註冊的 email 和密碼登入

### 案件管理

- **查看案件列表**: 首頁顯示所有案件
- **搜尋案件**: 使用搜尋欄位進行模糊搜尋
- **篩選案件**: 依狀態、縣市、鄉鎮區里篩選
- **排序案件**: 選擇不同的排序方式
- **建立案件**: 點擊「新建案件」按鈕
- **編輯案件**: 點擊案件列表中的編輯按鈕
- **刪除案件**: 點擊案件列表中的刪除按鈕

### 測試帳號

系統已預設以下測試帳號：

- **管理員**: ryowu@gmail.com
- **一般用戶**: sosan@example.com, shen@example.com, wu@example.com

## 資料模型

### 用戶模型 (CustomUser)

- email: 電子郵件 (主要登入欄位)
- username: 用戶名稱
- first_name, last_name: 姓名
- phone: 電話
- department: 部門

### 案件模型 (YfCase)

- yfcaseCaseNumber: 案號 (\*)
- yfcaseCompany: 所屬公司
- yfcaseCity: 縣市 (外鍵)
- yfcaseTownship: 鄉鎮區里 (外鍵)
- yfcaseStreet: 街路
- yfcaseLane: 巷
- yfcaseAlley: 弄
- yfcaseNumber: 號
- yfcaseFloor: 樓層
- yfcaseCaseStatus: 案件狀態
- user: 區域負責人 (外鍵)
- yfcaseTimestamp: 建立時間
- yfcaseUpdated: 更新時間

## 專案結構

```
case_management/
├── case_management/          # 專案設定
│   ├── settings.py          # Django設定
│   ├── urls.py              # 主要URL配置
│   └── wsgi.py              # WSGI配置
├── cases/                   # 案件應用
│   ├── models.py            # 案件相關模型
│   ├── views.py             # 視圖函數
│   ├── forms.py             # 表單類別
│   ├── urls.py              # URL配置
│   └── admin.py             # 管理員介面
├── users/                   # 用戶應用
│   ├── models.py            # 自定義用戶模型
│   └── admin.py             # 用戶管理員介面
├── templates/               # 模板目錄
│   ├── base.html            # 基礎模板
│   └── cases/               # 案件模板
├── static/                  # 靜態檔案
├── create_test_data.py      # 測試資料腳本
└── manage.py                # Django管理腳本
```

## 開發說明

### 新增功能

1. 在 `cases/models.py` 中新增模型欄位
2. 執行 `python manage.py makemigrations`
3. 執行 `python manage.py migrate`
4. 更新相關的視圖和模板

### 自訂樣式

- 主要樣式在 `templates/base.html` 中定義
- 可新增自訂 CSS 檔案到 `static/css/` 目錄

### 部署注意事項

- 修改 `settings.py` 中的 `SECRET_KEY`
- 設定 `DEBUG = False`
- 配置生產環境資料庫
- 設定靜態檔案服務

## 授權

本專案僅供學習和開發使用。

## 聯絡資訊

如有問題或建議，請聯繫開發團隊。
