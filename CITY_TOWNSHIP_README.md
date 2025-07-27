# 縣市鄉鎮聯動下拉式選單功能

## 功能概述

本專案已成功實作了縣市鄉鎮聯動下拉式選單功能，適用於以下兩個頁面：

- `templates/cases/case_form.html` - 案件表單的 `yfcaseCity` 和 `yfcaseTownship` 欄位
- `templates/account/profile.html` - 個人資料表單的 `userCountry` 和 `userTownship` 欄位

## 主要變更

### 1. 模型變更

#### YfCase 模型 (`cases/models.py`)

```python
# 原本的 ForeignKey 欄位
yfcaseCity = models.ForeignKey(City, verbose_name=u'縣市', on_delete=models.SET_NULL, null=True)
yfcaseTownship = models.ForeignKey(Township, verbose_name=u'鄉鎮區里', on_delete=models.SET_NULL, null=True)

# 改為 CharField 文字欄位
yfcaseCity = models.CharField(u'縣市', max_length=50, null=True, blank=True)
yfcaseTownship = models.CharField(u'鄉鎮區里', max_length=50, null=True, blank=True)
```

#### CustomUser 模型 (`users/models.py`)

```python
# 原本的 ForeignKey 欄位
userCountry = models.ForeignKey('cases.City', verbose_name=u'縣市', on_delete=models.SET_NULL, null=True, blank=True)
userTownship = models.ForeignKey('cases.Township', verbose_name=u'鄉鎮', on_delete=models.SET_NULL, null=True, blank=True)

# 改為 CharField 文字欄位
userCountry = models.CharField(u'縣市', max_length=50, null=True, blank=True)
userTownship = models.CharField(u'鄉鎮', max_length=50, null=True, blank=True)
```

### 2. JavaScript 實作

創建了 `static/js/cityTownship.js` 檔案，提供通用的縣市鄉鎮聯動功能：

#### 主要功能

- `CityTownshipSelector` 類別：處理縣市鄉鎮聯動邏輯
- 自動初始化：根據頁面中的元素自動初始化對應的選擇器
- AJAX 請求：動態載入鄉鎮選項
- 初始值處理：支援編輯時的正確顯示

#### 核心方法

- `updateTownships()`: 根據選中的縣市更新鄉鎮選項
- `setInitialValues()`: 設定初始選中的值
- `getSelectedValues()`: 獲取當前選中的值
- `clear()`: 清空選擇

### 3. API 端點

修改了 `cases/views.py` 中的 `get_townships` 函數：

```python
def get_townships(request):
    """AJAX: 根據縣市取得鄉鎮區里選項"""
    city_name = request.GET.get('city_id')  # 參數名稱保持不變，但實際傳遞的是縣市名稱
    if city_name:
        try:
            city = City.objects.get(name=city_name)
            townships = Township.objects.filter(city=city)
            data = [{'id': t.name, 'name': t.name} for t in townships]  # 使用鄉鎮名稱作為ID
            return JsonResponse(data, safe=False)
        except City.DoesNotExist:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)
```

### 4. 模板修改

#### 案件表單 (`templates/cases/case_form.html`)

- 將縣市和鄉鎮欄位改為自定義的 `<select>` 元素
- 引入 `cityTownship.js` 檔案
- 移除原有的 jQuery 聯動程式碼

#### 個人資料表單 (`templates/account/profile.html`)

- 將縣市和鄉鎮欄位改為自定義的 `<select>` 元素
- 引入 `cityTownship.js` 檔案
- 移除原有的 jQuery 聯動程式碼

### 5. Views 修改

#### 案件相關 Views (`cases/views.py`)

- 在 `case_create` 和 `case_update` 中傳遞縣市資料到模板
- 修改 API 端點以支援縣市名稱查詢

#### 用戶相關 Views (`users/views.py`)

- 在 `profile_edit` 中傳遞縣市資料到模板

## 使用方法

### 1. 在案件表單中使用

```html
<!-- 縣市選擇 -->
<select name="yfcaseCity" id="id_yfcaseCity" class="form-select" required>
    <option value="">請選擇縣市</option>
    {% for city in cities %}
        <option value="{{ city.name }}" {% if form.yfcaseCity.value == city.name %}selected{% endif %}>{{ city.name }}</option>
    {% endfor %}
</select>

<!-- 鄉鎮選擇 -->
<select name="yfcaseTownship" id="id_yfcaseTownship" class="form-select" required>
    <option value="">請選擇鄉鎮</option>
</select>
```

### 2. 在個人資料表單中使用

```html
<!-- 縣市選擇 -->
<select name="userCountry" id="id_userCountry" class="form-select">
    <option value="">請選擇縣市</option>
    {% for city in cities %}
        <option value="{{ city.name }}" {% if form.userCountry.value == city.name %}selected{% endif %}>{{ city.name }}</option>
    {% endfor %}
</select>

<!-- 鄉鎮選擇 -->
<select name="userTownship" id="id_userTownship" class="form-select">
    <option value="">請選擇鄉鎮</option>
</select>
```

### 3. 引入 JavaScript

```html
{% load static %} {% block extra_js %}
<script src="{% static 'js/cityTownship.js' %}"></script>
{% endblock %}
```

## 資料遷移

由於將 ForeignKey 欄位改為 CharField，舊的資料需要遷移。已提供 `migrate_city_township_data.py` 腳本來處理：

```bash
python migrate_city_township_data.py
```

## 測試

使用 `test_city_township.py` 腳本來測試功能：

```bash
python test_city_township.py
```

## 優點

1. **統一性**: 使用同一個 JavaScript 檔案處理兩個不同頁面的聯動功能
2. **可維護性**: 程式碼集中管理，易於維護和更新
3. **效能**: 使用原生 JavaScript fetch API，效能更好
4. **相容性**: 支援編輯時的初始值顯示
5. **擴展性**: 容易擴展到其他需要縣市鄉鎮聯動的頁面

## 注意事項

1. 確保資料庫中有縣市和鄉鎮的資料
2. 縣市名稱必須與資料庫中的名稱完全匹配
3. 鄉鎮選項會根據選中的縣市動態載入
4. 編輯時會自動載入對應的鄉鎮選項
