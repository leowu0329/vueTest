#!/usr/bin/env python
import os
import django

# 設定Django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_management.settings')
django.setup()

from cases.models import City, Township, YfCase
from users.models import CustomUser

def create_test_data():
    print("開始建立測試資料...")
    
    # 建立縣市
    cities_data = [
        '台北市', '新北市', '桃園市', '台中市', '台南市', '高雄市', '基隆市', '新竹市', '新竹縣', '苗栗縣',
        '彰化縣', '南投縣', '雲林縣', '嘉義市', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣'
    ]
    
    cities = {}
    for city_name in cities_data:
        city, created = City.objects.get_or_create(name=city_name)
        cities[city_name] = city
        if created:
            print(f"建立縣市: {city_name}")
    
    # 建立鄉鎮區里（以幾個主要城市為例）
    townships_data = {
        '台北市': ['中正區', '大同區', '中山區', '松山區', '大安區', '萬華區', '信義區', '士林區', '北投區', '內湖區', '南港區', '文山區'],
        '新北市': ['板橋區', '三重區', '中和區', '永和區', '新莊區', '新店區', '樹林區', '鶯歌區', '三峽區', '淡水區', '汐止區', '瑞芳區'],
        '台中市': ['中區', '東區', '南區', '西區', '北區', '西屯區', '南屯區', '北屯區', '豐原區', '東勢區', '大甲區', '清水區'],
        '台南市': ['中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區'],
        '高雄市': ['楠梓區', '左營區', '鼓山區', '三民區', '鹽埕區', '前金區', '新興區', '苓雅區', '前鎮區', '旗津區', '小港區', '鳳山區']
    }
    
    townships = {}
    for city_name, township_names in townships_data.items():
        if city_name in cities:
            for township_name in township_names:
                township, created = Township.objects.get_or_create(
                    name=township_name,
                    city=cities[city_name]
                )
                townships[f"{city_name}-{township_name}"] = township
                if created:
                    print(f"建立鄉鎮區里: {city_name} - {township_name}")
    
    # 建立測試用戶
    users_data = [
        {'email': 'sosan@example.com', 'username': 'sosan', 'first_name': 'Sosan', 'last_name': 'Chen'},
        {'email': 'shen@example.com', 'username': 'shen', 'first_name': '沈欣宜', 'last_name': 'Shen'},
        {'email': 'wu@example.com', 'username': 'wu', 'first_name': '吳俊男', 'last_name': 'Wu'},
    ]
    
    users = {}
    for user_data in users_data:
        user, created = CustomUser.objects.get_or_create(
            email=user_data['email'],
            defaults=user_data
        )
        users[user_data['email']] = user
        if created:
            print(f"建立用戶: {user_data['email']}")
    
    # 建立測試案件
    cases_data = [
        {
            'yfcaseCaseNumber': '非法拍案件',
            'yfcaseCompany': '揚富開發有限公司',
            'yfcaseCity': cities['台南市'],
            'yfcaseTownship': townships.get('台南市-北區'),
            'yfcaseStreet': '開元路',
            'yfcaseLane': '148',
            'yfcaseAlley': '101',
            'yfcaseNumber': '28',
            'yfcaseCaseStatus': '在途',
            'user': users['sosan@example.com']
        },
        {
            'yfcaseCaseNumber': '114年度司執字第23394號',
            'yfcaseCompany': '揚富開發有限公司',
            'yfcaseCity': cities['高雄市'],
            'yfcaseTownship': townships.get('高雄市-左營區'),
            'yfcaseStreet': '高鐵路',
            'yfcaseNumber': '116',
            'yfcaseCaseStatus': '在途',
            'user': users['shen@example.com']
        },
        {
            'yfcaseCaseNumber': '114年度司執字第30924號(好時價估4920000)',
            'yfcaseCompany': '鉅鈦開發有限公司',
            'yfcaseCity': cities['台北市'],
            'yfcaseTownship': townships.get('台北市-大安區'),
            'yfcaseStreet': '信義路',
            'yfcaseLane': '5',
            'yfcaseNumber': '7',
            'yfcaseFloor': '3樓',
            'yfcaseCaseStatus': '在途',
            'user': users['wu@example.com']
        },
        {
            'yfcaseCaseNumber': '113年度司執字第12345號',
            'yfcaseCompany': '揚富開發有限公司',
            'yfcaseCity': cities['台中市'],
            'yfcaseTownship': townships.get('台中市-西屯區'),
            'yfcaseStreet': '台灣大道',
            'yfcaseLane': '99',
            'yfcaseNumber': '88',
            'yfcaseFloor': '15樓之1',
            'yfcaseCaseStatus': '結案',
            'user': users['sosan@example.com']
        },
        {
            'yfcaseCaseNumber': '112年度司執字第98765號',
            'yfcaseCompany': '鉅鈦開發有限公司',
            'yfcaseCity': cities['新北市'],
            'yfcaseTownship': townships.get('新北市-板橋區'),
            'yfcaseStreet': '文化路',
            'yfcaseLane': '200',
            'yfcaseNumber': '50',
            'yfcaseCaseStatus': '結案',
            'user': users['shen@example.com']
        }
    ]
    
    for case_data in cases_data:
        case, created = YfCase.objects.get_or_create(
            yfcaseCaseNumber=case_data['yfcaseCaseNumber'],
            defaults=case_data
        )
        if created:
            print(f"建立案件: {case_data['yfcaseCaseNumber']}")
    
    print("測試資料建立完成！")

if __name__ == '__main__':
    create_test_data() 