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

    townships_data = {
    '台北市': ['中正區', '大同區', '中山區', '松山區', '大安區', '萬華區', '信義區', '士林區', '北投區', '內湖區', '南港區', '文山區'],
    '新北市': ['板橋區', '三重區', '中和區', '永和區', '新莊區', '新店區', '樹林區', '鶯歌區', '三峽區', '淡水區', '汐止區', '瑞芳區', '土城區', '蘆洲區', '五股區', '泰山區', '林口區', '深坑區', '石碇區', '坪林區', '三芝區', '石門區', '八里區', '平溪區', '雙溪區', '貢寮區', '金山區', '萬里區', '烏來區'],
    '桃園市': ['桃園區', '中壢區', '平鎮區', '八德區', '楊梅區', '蘆竹區', '大溪區', '龍潭區', '龜山區', '大園區', '觀音區', '新屋區', '復興區'],
    '台中市': ['中區', '東區', '南區', '西區', '北區', '西屯區', '南屯區', '北屯區', '豐原區', '東勢區', '大甲區', '清水區', '沙鹿區', '梧棲區', '后里區', '神岡區', '潭子區', '大雅區', '新社區', '石岡區', '和平區', '大肚區', '烏日區', '龍井區', '霧峰區', '太平區', '大里區', '外埔區'],
    '台南市': ['中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '安定區'],
    '高雄市': ['楠梓區', '左營區', '鼓山區', '三民區', '鹽埕區', '前金區', '新興區', '苓雅區', '前鎮區', '旗津區', '小港區', '鳳山區', '林園區', '大寮區', '大樹區', '大社區', '仁武區', '鳥松區', '岡山區', '橋頭區', '燕巢區', '田寮區', '阿蓮區', '路竹區', '湖內區', '茄萣區', '永安區', '彌陀區', '梓官區', '旗山區', '美濃區', '六龜區', '甲仙區', '杉林區', '內門區', '茂林區', '桃源區', '那瑪夏區'],
    '基隆市': ['仁愛區', '信義區', '中正區', '中山區', '安樂區', '暖暖區', '七堵區'],
    '新竹市': ['東區', '北區', '香山區'],
    '新竹縣': ['竹北市', '竹東鎮', '新埔鎮', '關西鎮', '湖口鄉', '新豐鄉', '芎林鄉', '橫山鄉', '北埔鄉', '寶山鄉', '峨眉鄉', '尖石鄉', '五峰鄉'],
    '苗栗縣': ['苗栗市', '頭份市', '竹南鎮', '後龍鎮', '通霄鎮', '苑裡鎮', '卓蘭鎮', '造橋鄉', '西湖鄉', '頭屋鄉', '公館鄉', '銅鑼鄉', '三義鄉', '大湖鄉', '獅潭鄉', '三灣鄉', '南庄鄉', '泰安鄉'],
    '彰化縣': ['彰化市', '員林市', '鹿港鎮', '和美鎮', '北斗鎮', '溪湖鎮', '田中鎮', '二林鎮', '線西鄉', '伸港鄉', '福興鄉', '秀水鄉', '花壇鄉', '芬園鄉', '大村鄉', '埔鹽鄉', '埔心鄉', '永靖鄉', '社頭鄉', '二水鄉', '田尾鄉', '埤頭鄉', '芳苑鄉', '大城鄉', '竹塘鄉', '溪州鄉'],
    '南投縣': ['南投市', '埔里鎮', '草屯鎮', '竹山鎮', '集集鎮', '名間鄉', '鹿谷鄉', '中寮鄉', '魚池鄉', '國姓鄉', '水里鄉', '信義鄉', '仁愛鄉'],
    '雲林縣': ['斗六市', '斗南鎮', '虎尾鎮', '西螺鎮', '土庫鎮', '北港鎮', '古坑鄉', '大埤鄉', '莿桐鄉', '林內鄉', '二崙鄉', '崙背鄉', '麥寮鄉', '東勢鄉', '褒忠鄉', '臺西鄉', '元長鄉', '四湖鄉', '口湖鄉', '水林鄉'],
    '嘉義市': ['東區', '西區'],
    '嘉義縣': ['太保市', '朴子市', '布袋鎮', '大林鎮', '民雄鄉', '溪口鄉', '新港鄉', '六腳鄉', '東石鄉', '義竹鄉', '鹿草鄉', '水上鄉', '中埔鄉', '竹崎鄉', '梅山鄉', '番路鄉', '大埔鄉', '阿里山鄉'],
    '屏東縣': ['屏東市', '潮州鎮', '東港鎮', '恆春鎮', '萬丹鄉', '長治鄉', '麟洛鄉', '九如鄉', '里港鄉', '鹽埔鄉', '高樹鄉', '萬巒鄉', '內埔鄉', '竹田鄉', '新埤鄉', '枋寮鄉', '新園鄉', '崁頂鄉', '林邊鄉', '南州鄉', '佳冬鄉', '琉球鄉', '車城鄉', '滿州鄉', '枋山鄉', '三地門鄉', '霧臺鄉', '瑪家鄉', '泰武鄉', '來義鄉', '春日鄉', '獅子鄉', '牡丹鄉'],
    '宜蘭縣': ['宜蘭市', '羅東鎮', '蘇澳鎮', '頭城鎮', '礁溪鄉', '壯圍鄉', '員山鄉', '冬山鄉', '五結鄉', '三星鄉', '大同鄉', '南澳鄉'],
    '花蓮縣': ['花蓮市', '鳳林鎮', '玉里鎮', '新城鄉', '吉安鄉', '壽豐鄉', '光復鄉', '豐濱鄉', '瑞穗鄉', '富里鄉', '秀林鄉', '萬榮鄉', '卓溪鄉'],
    '台東縣': ['臺東市', '成功鎮', '關山鎮', '卑南鄉', '鹿野鄉', '池上鄉', '東河鄉', '長濱鄉', '太麻里鄉', '大武鄉', '綠島鄉', '海端鄉', '延平鄉', '金峰鄉', '達仁鄉', '蘭嶼鄉'],
    '澎湖縣': ['馬公市', '湖西鄉', '白沙鄉', '西嶼鄉', '望安鄉', '七美鄉'],
    '金門縣': ['金城鎮', '金沙鎮', '金湖鎮', '金寧鄉', '烈嶼鄉', '烏坵鄉'],
    '連江縣': ['南竿鄉', '北竿鄉', '莒光鄉', '東引鄉']
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
        {'email': 'sosan@example.com', 'username': 'sosan', 'first_name': 'Sosan', 'last_name': 'Chen', 'userFullName': 'Sosan Chen'},
        {'email': 'shen@example.com', 'username': 'shen', 'first_name': '沈欣宜', 'last_name': 'Shen', 'userFullName': '沈欣宜'},
        {'email': 'wu@example.com', 'username': 'wu', 'first_name': '吳俊男', 'last_name': 'Wu', 'userFullName': '吳俊男'},
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