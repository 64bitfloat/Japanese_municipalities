import json

print("Reading raw_localgovjp.json...")
with open("raw_localgovjp.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total raw entries: {len(data)}")

# Designated cities (政令指定都市 20市) JIS 5-digit code -> Name
DESIGNATED_CITIES = {
    "01100": "札幌市",
    "04100": "仙台市",
    "11100": "さいたま市",
    "12100": "千葉市",
    "14100": "横浜市",
    "14130": "川崎市",
    "14150": "相模原市",
    "15100": "新潟市",
    "22100": "静岡市",
    "22130": "浜松市",
    "23100": "名古屋市",
    "26100": "京都市",
    "27100": "大阪市",
    "27140": "堺市",
    "28100": "神戸市",
    "33100": "岡山市",
    "34100": "広島市",
    "40100": "北九州市",
    "40130": "福岡市",
    "43100": "熊本市",
}

# Prefectures capital cities (都道府県庁所在地 47市/区)
CAPITAL_NAMES = {
    "札幌市", "青森市", "盛岡市", "仙台市", "秋田市", "山形市", "福島市",
    "水戸市", "宇都宮市", "前橋市", "さいたま市", "千葉市", "新宿区",
    "横浜市", "新潟市", "富山市", "金沢市", "福井市", "甲府市", "長野市",
    "岐阜市", "静岡市", "名古屋市", "津市", "大津市", "京都市", "大阪市",
    "神戸市", "奈良市", "和歌山市", "鳥取市", "松江市", "岡山市", "広島市",
    "山口市", "徳島市", "高松市", "松山市", "高知市", "福岡市", "佐賀市",
    "長崎市", "熊本市", "大分市", "宮崎市", "鹿児島市", "那覇市"
}

# Core cities (中核市 62市)
CORE_CITIES = {
    "旭川市", "函館市", "青森市", "八戸市", "盛岡市", "秋田市", "山形市", "福島市", "郡山市", "いわき市",
    "水戸市", "宇都宮市", "前橋市", "高崎市", "川越市", "川口市", "越谷市", "船橋市", "柏市", "八王子市",
    "横須賀市", "富山市", "金沢市", "福井市", "甲府市", "長野市", "松本市", "岐阜市", "豊橋市", "岡崎市",
    "一宮市", "豊田市", "大津市", "豊中市", "吹田市", "高槻市", "枚方市", "寝屋川市", "八尾市", "東大阪市",
    "姫路市", "尼崎市", "明石市", "西宮市", "奈良市", "和歌山市", "鳥取市", "松江市", "倉敷市", "福山市",
    "呉市", "下関市", "高松市", "松山市", "高知市", "久留米市", "長崎市", "佐世保市", "大分市", "宮崎市",
    "鹿児島市", "那覇市"
}

# Special cities at time of enforcement (施行時特例市 23市)
SPECIAL_CITIES = {
    "つくば市", "伊勢崎市", "太田市", "所沢市", "草加市", "熊谷市", "春日部市",
    "小田原市", "大和市", "平塚市", "厚木市", "茅ヶ崎市", "長岡市", "上越市",
    "富士市", "沼津市", "春日井市", "四日市市", "茨木市", "岸和田市",
    "加古川市", "宝塚市", "佐賀市"
}

# Administrative wards mapping to designated city
WARD_TO_CITY = {}
# 札幌市 01100
for c in range(1101, 1111): WARD_TO_CITY[f"0{c}"] = "01100"
# 仙台市 04100
for c in range(4101, 4106): WARD_TO_CITY[f"0{c}"] = "04100"
# さいたま市 11100
for c in range(11101, 11111): WARD_TO_CITY[str(c)] = "11100"
# 千葉市 12100
for c in range(12101, 12107): WARD_TO_CITY[str(c)] = "12100"
# 横浜市 14100
for c in range(14101, 14119): WARD_TO_CITY[str(c)] = "14100"
# 川崎市 14130
for c in range(14131, 14138): WARD_TO_CITY[str(c)] = "14130"
# 相模原市 14150
for c in range(14151, 14154): WARD_TO_CITY[str(c)] = "14150"
# 新潟市 15100
for c in range(15101, 15109): WARD_TO_CITY[str(c)] = "15100"
# 静岡市 22100
for c in range(22101, 22104): WARD_TO_CITY[str(c)] = "22100"
# 浜松市 22130
for c in range(22131, 22141): WARD_TO_CITY[str(c)] = "22130"
# 名古屋市 23100
for c in range(23101, 23117): WARD_TO_CITY[str(c)] = "23100"
# 京都市 26100
for c in range(26101, 26112): WARD_TO_CITY[str(c)] = "26100"
# 大阪市 27100 (27102 - 27128)
for c in range(27102, 27129): WARD_TO_CITY[str(c)] = "27100"
# 堺市 27140
for c in range(27141, 27148): WARD_TO_CITY[str(c)] = "27140"
# 神戸市 28100
for c in range(28101, 28112): WARD_TO_CITY[str(c)] = "28100"
# 岡山市 33100
for c in range(33101, 33105): WARD_TO_CITY[str(c)] = "33100"
# 広島市 34100
for c in range(34101, 34109): WARD_TO_CITY[str(c)] = "34100"
# 北九州市 40100 (40101: 門司, 40103: 若松, 40105: 戸畑, 40106: 小倉北, 40107: 小倉南, 40108: 八幡東, 40109: 八幡西)
for c in range(40101, 40110): WARD_TO_CITY[str(c)] = "40100"
# 福岡市 40130
for c in range(40131, 40138): WARD_TO_CITY[str(c)] = "40130"
# 熊本市 43100
for c in range(43101, 43106): WARD_TO_CITY[str(c)] = "43100"

# 追加主要都市リスト（Level 1最低4都市保証用）
PROMOTED_CITIES = {
    "苫小牧市", # 北海道
    "奥州市", "一関市", "花巻市", # 岩手
    "石巻市", "大崎市", "登米市", # 宮城
    "横手市", "大仙市", "由利本荘市", # 秋田
    "鶴岡市", "酒田市", "米沢市", # 山形
    "日立市", "ひたちなか市", # 茨城
    "小山市", "栃木市", "足利市", # 栃木
    "市川市", "松戸市", # 千葉
    "三条市", # 新潟
    "白山市", "小松市", "加賀市", # 石川
    "甲斐市", "南アルプス市", "笛吹市", # 山梨
    "上田市", "飯田市", # 長野
    "大垣市", "各務原市", "多治見市", # 岐阜
    "鈴鹿市", "松阪市", # 三重
    "草津市", "長浜市", "彦根市", # 滋賀
    "宇治市", "亀岡市", "舞鶴市", # 京都
    "橿原市", "生駒市", "大和郡山市", # 奈良
    "津山市", "総社市", # 岡山
    "東広島市", # 広島
    "宇部市", "周南市", # 山口
    "今治市", "新居浜市", "西条市", # 愛媛
    "南国市", "四万十市", "香南市", # 高知
    "飯塚市", # 福岡
    "諫早市", "大村市", # 長崎
    "八代市", "天草市", "玉名市", # 熊本
    "別府市", "中津市", "日田市", # 大分
    "霧島市", "鹿屋市", "薩摩川内市", # 鹿児島
    "沖縄市", "うるま市", "浦添市", # 沖縄
}

# 市の総数が10件以下の都道府県コード（Level 1に市全域を統合）
SMALL_CITY_PREFS = {
    "02", # 青森 (10)
    "16", # 富山 (10)
    "18", # 福井 (9)
    "30", # 和歌山 (9)
    "31", # 鳥取 (4)
    "32", # 島根 (8)
    "36", # 徳島 (8)
    "37", # 香川 (8)
    "41", # 佐賀 (10)
    "45", # 宮崎 (9)
}

municipalities = {}

for item in data:
    lgcode = str(item.get('lgcode', ''))
    if len(lgcode) >= 5:
        code5 = lgcode[:5]
    else:
        continue

    pref = item.get('pref', '')
    city = item.get('city', '')
    kana = item.get('citykana', '')
    lat = item.get('lat', None)
    lng = item.get('lng', None)

    # Skip prefecture level entries
    if not city or (code5.endswith('000') and code5 not in DESIGNATED_CITIES):
        continue

    # Skip administrative wards of designated cities
    if code5 in WARD_TO_CITY:
        continue

    pref_code = code5[:2]

    # Special wards (Tokyo 23 wards: 13101 - 13123)
    if pref_code == '13' and 13101 <= int(code5) <= 13123:
        m_type = 'ward'
    elif city.endswith('市'):
        m_type = 'city'
    elif city.endswith('町'):
        m_type = 'town'
    elif city.endswith('村'):
        m_type = 'village'
    elif city.endswith('区'):
        m_type = 'ward'
    else:
        continue

    # Determine Level & Subtype
    # ルール1: 東京都の例外指定
    if pref_code == '13':
        if m_type == 'ward':
            level = 1
            sub_type = 'ward'
        elif m_type == 'city':
            level = 2
            sub_type = 'city' # 八王子市も含めて多摩地域26市はLevel 2
        elif m_type == 'town':
            level = 3
            sub_type = 'town'
        else: # village
            level = 4
            sub_type = 'village'
    # ルール3: 市が10件以下の都道府県は、市全域をLevel 1に統合
    elif pref_code in SMALL_CITY_PREFS and m_type == 'city':
        level = 1
        sub_type = 'city_all'
    elif m_type == 'city':
        # ルール4: 主要都市（政令市・県庁・中核市・特例市・昇格指定都市）はLevel 1
        if code5 in DESIGNATED_CITIES or city in CAPITAL_NAMES or city in CORE_CITIES or city in SPECIAL_CITIES or city in PROMOTED_CITIES:
            level = 1
            sub_type = 'designated' if code5 in DESIGNATED_CITIES else ('capital' if city in CAPITAL_NAMES else ('core' if city in CORE_CITIES else 'major'))
        else:
            level = 2
            sub_type = 'city'
    elif m_type == 'town':
        level = 3
        sub_type = 'town'
    else: # village
        level = 4
        sub_type = 'village'

    municipalities[code5] = {
        'c': code5,
        'p': pref_code,
        'pref': pref,
        'n': city,
        'k': kana,
        't': sub_type,
        'm_type': m_type,
        'lvl': level,
        'lat': float(lat) if lat else None,
        'lng': float(lng) if lng else None
    }

# Ensure all 20 designated cities are present
for d_code, d_name in DESIGNATED_CITIES.items():
    if d_code not in municipalities:
        pref_c = d_code[:2]
        sample = next((m for m in municipalities.values() if m['p'] == pref_c), None)
        p_name = sample['pref'] if sample else ""
        municipalities[d_code] = {
            'c': d_code,
            'p': pref_c,
            'pref': p_name,
            'n': d_name,
            'k': "",
            't': 'designated',
            'm_type': 'city',
            'lvl': 1,
            'lat': None,
            'lng': None
        }

t_counts = {'city': 0, 'ward': 0, 'town': 0, 'village': 0}
for m in municipalities.values():
    t_counts[m['m_type']] += 1

print("\n--- Municipalities count breakdown ---")
print(f"Cities (市): {t_counts['city']} (Target: 792)")
print(f"Special Wards (特別区): {t_counts['ward']} (Target: 23)")
print(f"Towns (町): {t_counts['town']} (Target: 743)")
print(f"Villages (村): {t_counts['village']} (Target: 183)")
total = sum(t_counts.values())
print(f"Total: {total} (Target: 1,741)")

# Save JSON
with open("municipalities.json", "w", encoding="utf-8") as f:
    json.dump(municipalities, f, ensure_ascii=False, indent=2)

with open("ward_to_city.json", "w", encoding="utf-8") as f:
    json.dump(WARD_TO_CITY, f, ensure_ascii=False, indent=2)

print("Saved municipalities.json and ward_to_city.json successfully.")
