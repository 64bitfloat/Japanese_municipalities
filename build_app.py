import json
import os

print("Building index.html with embedded municipality dataset...")

# Load master data
with open("municipalities.json", "r", encoding="utf-8") as f:
    muni_data = json.load(f)

with open("ward_to_city.json", "r", encoding="utf-8") as f:
    ward_to_city = json.load(f)

# Compact array format: [code, pref_code, pref_name, name, kana, type, lvl, lat, lng]
muni_arr = []
for m in muni_data.values():
    muni_arr.append([
        m['c'],
        m['p'],
        m['pref'],
        m['n'],
        m['k'],
        m['t'],
        m['lvl'],
        round(m['lat'], 4) if m['lat'] else None,
        round(m['lng'], 4) if m['lng'] else None
    ])

print(f"Total municipalities for embed: {len(muni_arr)}")
print(f"Total ward mappings: {len(ward_to_city)}")

# Prefecture master
PREFECTURES = [
    {"code": "01", "name": "北海道", "region": "北海道", "islands": [{"label": "全域", "bounds": [[41.3, 139.3], [45.6, 145.9]]}, {"label": "利尻・礼文", "bounds": [[45.0, 140.9], [45.5, 141.4]]}]},
    {"code": "02", "name": "青森県", "region": "東北"},
    {"code": "03", "name": "岩手県", "region": "東北"},
    {"code": "04", "name": "宮城県", "region": "東北"},
    {"code": "05", "name": "秋田県", "region": "東北"},
    {"code": "06", "name": "山形県", "region": "東北"},
    {"code": "07", "name": "福島県", "region": "東北"},
    {"code": "08", "name": "茨城県", "region": "関東"},
    {"code": "09", "name": "栃木県", "region": "関東"},
    {"code": "10", "name": "群馬県", "region": "関東"},
    {"code": "11", "name": "埼玉県", "region": "関東"},
    {"code": "12", "name": "千葉県", "region": "関東"},
    {"code": "13", "name": "東京都", "region": "関東", "defaultView": [[35.5, 138.9], [35.9, 139.9]], "islands": [{"label": "全域", "bounds": [[24.0, 138.9], [35.9, 142.3]]}, {"label": "本土", "bounds": [[35.5, 138.9], [35.9, 139.9]]}, {"label": "伊豆諸島", "bounds": [[32.4, 138.9], [34.8, 140.2]]}, {"label": "小笠原諸島", "bounds": [[24.0, 141.9], [27.3, 142.3]]}]},
    {"code": "14", "name": "神奈川県", "region": "関東"},
    {"code": "15", "name": "新潟県", "region": "中部", "defaultView": [[36.7, 137.6], [38.6, 139.9]], "islands": [{"label": "全域", "bounds": [[36.7, 137.6], [38.6, 139.9]]}, {"label": "本土", "bounds": [[36.7, 137.6], [38.6, 139.9]]}, {"label": "佐渡・粟島", "bounds": [[37.7, 138.1], [38.6, 139.3]]}]},
    {"code": "16", "name": "富山県", "region": "中部"},
    {"code": "17", "name": "石川県", "region": "中部"},
    {"code": "18", "name": "福井県", "region": "中部"},
    {"code": "19", "name": "山梨県", "region": "中部"},
    {"code": "20", "name": "長野県", "region": "中部"},
    {"code": "21", "name": "岐阜県", "region": "中部"},
    {"code": "22", "name": "静岡県", "region": "中部"},
    {"code": "23", "name": "愛知県", "region": "中部"},
    {"code": "24", "name": "三重県", "region": "近畿"},
    {"code": "25", "name": "滋賀県", "region": "近畿"},
    {"code": "26", "name": "京都府", "region": "近畿"},
    {"code": "27", "name": "大阪府", "region": "近畿"},
    {"code": "28", "name": "兵庫県", "region": "近畿"},
    {"code": "29", "name": "奈良県", "region": "近畿"},
    {"code": "30", "name": "和歌山県", "region": "近畿"},
    {"code": "31", "name": "鳥取県", "region": "中国"},
    {"code": "32", "name": "島根県", "region": "中国", "defaultView": [[34.3, 131.6], [35.6, 133.4]], "islands": [{"label": "全域", "bounds": [[34.3, 131.6], [36.4, 133.4]]}, {"label": "本土", "bounds": [[34.3, 131.6], [35.6, 133.4]]}, {"label": "隠岐諸島", "bounds": [[35.9, 132.9], [36.4, 133.4]]}]},
    {"code": "33", "name": "岡山県", "region": "中国"},
    {"code": "34", "name": "広島県", "region": "中国"},
    {"code": "35", "name": "山口県", "region": "中国"},
    {"code": "36", "name": "徳島県", "region": "四国"},
    {"code": "37", "name": "香川県", "region": "四国"},
    {"code": "38", "name": "愛媛県", "region": "四国"},
    {"code": "39", "name": "高知県", "region": "四国"},
    {"code": "40", "name": "福岡県", "region": "九州・沖縄"},
    {"code": "41", "name": "佐賀県", "region": "九州・沖縄"},
    {"code": "42", "name": "長崎県", "region": "九州・沖縄", "defaultView": [[32.5, 129.7], [33.4, 130.4]], "islands": [{"label": "全域", "bounds": [[32.5, 128.5], [34.7, 130.4]]}, {"label": "本土", "bounds": [[32.5, 129.7], [33.4, 130.4]]}, {"label": "対馬", "bounds": [[34.0, 129.1], [34.7, 129.5]]}, {"label": "壱岐", "bounds": [[33.7, 129.6], [33.9, 129.8]]}, {"label": "五島列島", "bounds": [[32.5, 128.5], [33.1, 129.2]]}]},
    {"code": "43", "name": "熊本県", "region": "九州・沖縄"},
    {"code": "44", "name": "大分県", "region": "九州・沖縄"},
    {"code": "45", "name": "宮崎県", "region": "九州・沖縄"},
    {"code": "46", "name": "鹿児島県", "region": "九州・沖縄", "defaultView": [[30.9, 130.0], [32.3, 131.2]], "islands": [{"label": "全域", "bounds": [[27.0, 128.3], [32.3, 131.2]]}, {"label": "本土", "bounds": [[30.9, 130.0], [32.3, 131.2]]}, {"label": "奄美群島", "bounds": [[27.0, 128.3], [28.6, 130.1]]}, {"label": "種子島・屋久島", "bounds": [[30.1, 130.3], [30.9, 131.1]]}]},
    {"code": "47", "name": "沖縄県", "region": "九州・沖縄", "defaultView": [[26.0, 127.5], [26.9, 128.4]], "islands": [{"label": "全域", "bounds": [[24.0, 122.9], [27.1, 128.4]]}, {"label": "沖縄本島", "bounds": [[26.0, 127.5], [26.9, 128.4]]}, {"label": "宮古・八重山", "bounds": [[24.0, 122.9], [25.0, 125.5]]}]}
]

muni_json_str = json.dumps(muni_arr, ensure_ascii=False, separators=(',', ':'))
ward_json_str = json.dumps(ward_to_city, ensure_ascii=False, separators=(',', ':'))
pref_json_str = json.dumps(PREFECTURES, ensure_ascii=False, separators=(',', ':'))

html_template = f'''<!DOCTYPE html>
<html lang="ja" class="h-full bg-slate-900 text-slate-100">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>GeoAnki JP — 全国1,741市区町村 視覚暗記トレーナー</title>

  <!-- 基本メタ情報 & OGP -->
  <meta name="description" content="全国1,741市区町村（792市・743町・183村・23特別区）を白地図ベクターポリゴンで直感暗記するWebアプリケーション。5桁JISコード完全バインド。" />
  <meta name="theme-color" content="#0f172a" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="GeoAnki JP — 全国1,741市区町村 視覚暗記トレーナー" />
  <meta property="og:description" content="全国1,741市区町村を白地図ベクターポリゴンで効率的に暗記！4段階難易度、3つの学習モード、島嶼部・極小自治体アシスト機能搭載。" />

  <!-- ファビコン -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%2310b981'/><text x='50' y='64' font-size='44' font-weight='900' fill='white' text-anchor='middle' font-family='sans-serif'>1741</text></svg>" />

  <!-- Tailwind CSS (CDN) -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#ecfdf5',
              100: '#d1fae5',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
            }}
          }}
        }}
      }}
    }};
  </script>

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <!-- Turf.js (政令指定都市の外郭ポリゴン自動結合) -->
  <script src="https://cdn.jsdelivr.net/npm/@turf/turf@6/turf.min.js"></script>

  <style>
    /* モバイルでの誤タッチ・ダブルタップズーム防止 */
    html, body, button, .no-dbltap {{
      touch-action: manipulation;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Kaku Gothic ProN", "Yu Gothic UI", sans-serif;
    }}
    /* 地図コンテナの背景色（ウォーターマークのない清潔な海色） */
    #map {{
      background: #090d16 !important;
    }}
    .leaflet-container {{
      background: #090d16 !important;
    }}
    /* 地図上のポリゴンパルスアニメーション */
    @keyframes pulse-yellow {{
      0%, 100% {{ fill-opacity: 0.95; stroke-width: 3px; }}
      50% {{ fill-opacity: 0.45; stroke-width: 4.5px; stroke: #eab308; }}
    }}
    .polygon-pulse {{
      animation: pulse-yellow 1.2s infinite ease-in-out;
    }}
    /* カスタムスクロールバー */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #0f172a;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #475569;
    }}
  </style>
</head>
<body class="h-full flex flex-col overflow-hidden bg-slate-900 select-none">

  <!-- ========================================== -->
  <!-- 画面A: 都道府県セレクト画面 (Hub) -->
  <!-- ========================================== -->
  <div id="screen-hub" class="flex-1 flex flex-col h-full overflow-hidden">
    <!-- Hub ヘッダー -->
    <header class="bg-slate-800/90 backdrop-blur border-b border-slate-700/80 px-4 py-3 shrink-0 z-10">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-3">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <span class="text-white font-black text-sm tracking-wider">JP</span>
          </div>
          <div>
            <h1 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
              GeoAnki 1741
              <span class="text-xs font-normal text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">JIS準拠</span>
            </h1>
            <p class="text-xs text-slate-400 hidden sm:block">全国1,741市区町村 視覚ベクター暗記トレーナー</p>
          </div>
        </div>

        <!-- 総合制覇率サマリー & アクション -->
        <div class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-xs text-slate-400">全国制覇数</div>
            <div class="text-sm sm:text-base font-extrabold text-emerald-400">
              <span id="hub-total-cleared">0</span> <span class="text-xs font-normal text-slate-400">/ 1,741</span>
              <span id="hub-total-pct" class="text-xs font-semibold text-slate-300 ml-1">(0.0%)</span>
            </div>
          </div>
          <button id="btn-show-help" class="p-2 rounded-lg bg-slate-700/60 hover:bg-slate-700 text-slate-300 hover:text-white transition" title="使い方ガイド">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </button>
        </div>
      </div>
    </header>

    <!-- 全国達成度プログレスバー -->
    <div class="w-full bg-slate-800/50 border-b border-slate-700/50 px-4 py-2 shrink-0">
      <div class="max-w-6xl mx-auto flex items-center gap-3">
        <div class="flex-1 bg-slate-700/60 h-2.5 rounded-full overflow-hidden">
          <div id="hub-progress-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-0 transition-all duration-500"></div>
        </div>
        <div class="text-xs font-semibold text-slate-300 shrink-0">
          全47都道府県中 <span id="hub-pref-completed-count" class="text-emerald-400 font-bold">0</span> 県コンプリート
        </div>
      </div>
    </div>

    <!-- 地方別フィルターピルバー -->
    <div class="bg-slate-900/90 border-b border-slate-800 px-4 py-2 shrink-0 overflow-x-auto no-scrollbar">
      <div class="max-w-6xl mx-auto flex gap-1.5 min-w-max" id="region-filter-bar">
        <button class="region-filter-btn px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500 text-white" data-region="ALL">すべて</button>
        <button class="region-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="北海道">北海道</button>
        <button class="region-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="東北">東北</button>
        <button class="region-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="関東">関東</button>
        <button class="region-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="中部">中部</button>
        <button class="region-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="近畿">近畿</button>
        <button class="region-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="中国">中国</button>
        <button class="region-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="四国">四国</button>
        <button class="region-filter-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-region="九州・沖縄">九州・沖縄</button>
      </div>
    </div>

    <!-- 都道府県カードグリッド (スクロール可能領域) -->
    <main class="flex-1 overflow-y-auto px-4 py-4">
      <div class="max-w-6xl mx-auto space-y-6" id="hub-pref-container">
        <!-- JSで地方別・都道府県カードを動的生成 -->
      </div>
    </main>
  </div>

  <!-- ========================================== -->
  <!-- 画面B: 都道府県別クイズ・学習画面 (Spoke) -->
  <!-- ========================================== -->
  <div id="screen-spoke" class="flex-1 flex flex-col h-full overflow-hidden hidden">
    <!-- Spoke 上部ヘッダー -->
    <header class="bg-slate-800/95 backdrop-blur border-b border-slate-700/80 px-3 py-2 shrink-0 z-20 flex items-center justify-between gap-2">
      <div class="flex items-center gap-2">
        <button id="btn-back-hub" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-xs sm:text-sm font-semibold text-white transition active:scale-95">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
          <span>戻る</span>
        </button>
        <div>
          <h2 class="text-sm sm:text-base font-bold text-white flex items-center gap-2">
            <span id="spoke-pref-name">都道府県名</span>
            <span id="spoke-pref-count-badge" class="text-xs font-medium text-slate-300 bg-slate-700/70 px-2 py-0.5 rounded-full">35自治体</span>
          </h2>
        </div>
      </div>

      <!-- 右側：進捗 & 音声設定 -->
      <div class="flex items-center gap-2">
        <div class="text-right hidden sm:block">
          <div class="text-xs text-slate-400">制覇状況</div>
          <div class="text-xs font-bold text-emerald-400">
            <span id="spoke-cleared-count">0</span> / <span id="spoke-total-count">0</span>
            <span id="spoke-cleared-pct" class="text-slate-300 font-normal ml-0.5">(0%)</span>
          </div>
        </div>
        <button id="btn-toggle-sound" class="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-300 hover:text-white transition" title="効果音切替">
          <svg id="icon-sound-on" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
          <svg id="icon-sound-off" class="w-4 h-4 hidden text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2"/></svg>
        </button>
      </div>
    </header>

    <!-- Spoke サブコントロールバー (難易度Levelタブ & 操作モード) -->
    <div class="bg-slate-900 border-b border-slate-800 px-3 py-1.5 shrink-0 flex flex-wrap items-center justify-between gap-2 z-10">
      <!-- 難易度Levelタブ -->
      <div class="flex items-center gap-1 overflow-x-auto no-scrollbar" id="level-tabs-container">
        <button class="level-tab-btn px-2.5 py-1 rounded text-xs font-semibold bg-emerald-500 text-white" data-level="1">
          <span class="tab-label">Lv.1 主要都市</span> <span class="tab-count font-normal opacity-80">(0)</span>
        </button>
        <button class="level-tab-btn px-2.5 py-1 rounded text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-level="2">
          <span class="tab-label">Lv.2 市</span> <span class="tab-count font-normal opacity-80">(0)</span>
        </button>
        <button class="level-tab-btn px-2.5 py-1 rounded text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-level="3">
          <span class="tab-label">Lv.3 町</span> <span class="tab-count font-normal opacity-80">(0)</span>
        </button>
        <button class="level-tab-btn px-2.5 py-1 rounded text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-level="4">
          <span class="tab-label">Lv.4 村</span> <span class="tab-count font-normal opacity-80">(0)</span>
        </button>
        <button class="level-tab-btn px-2.5 py-1 rounded text-xs font-medium bg-slate-800 text-slate-300 hover:bg-slate-700" data-level="ALL">
          <span class="tab-label">全自治体</span> <span class="tab-count font-normal opacity-80">(0)</span>
        </button>
        <button class="level-tab-btn px-2.5 py-1 rounded text-xs font-medium bg-rose-950/40 text-rose-300 border border-rose-800/50 hover:bg-rose-900/40 hidden" data-level="WEAK">
          <span class="tab-label">⚠️ 弱点復習</span> <span id="weak-tab-count" class="tab-count font-bold">(0)</span>
        </button>
      </div>

      <!-- 操作モード切替セグメント -->
      <div class="flex items-center bg-slate-800 p-0.5 rounded-lg border border-slate-700">
        <button class="mode-tab-btn px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-700 text-emerald-400 shadow" data-mode="locate" title="場所当てクイズ">
          🎯 場所当て
        </button>
        <button class="mode-tab-btn px-2.5 py-1 rounded-md text-xs font-medium text-slate-300 hover:text-white" data-mode="name" title="名前当て4択">
          🔤 名前当て
        </button>
        <button class="mode-tab-btn px-2.5 py-1 rounded-md text-xs font-medium text-slate-300 hover:text-white" data-mode="explore" title="自由閲覧モード">
          🔍 探索
        </button>
      </div>
    </div>

    <!-- 地図コンテナ & オーバーレイ -->
    <div class="flex-1 relative overflow-hidden bg-slate-950">
      <!-- Leaflet 地図エレメント -->
      <div id="map" class="w-full h-full z-0"></div>

      <!-- 地図上フローティング救済UI（島嶼部ズーム & フォーカス） -->
      <div class="absolute top-3 right-3 z-10 flex flex-col gap-2 items-end">
        <!-- 島嶼部クイックズームボタン群 (対象県でのみ動的生成) -->
        <div id="island-buttons-container" class="flex flex-col gap-1 items-end"></div>

        <!-- 虫眼鏡（フォーカス）アシストボタン -->
        <button id="btn-focus-current" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/90 hover:bg-slate-700 text-white border border-slate-600/70 shadow-lg backdrop-blur text-xs font-semibold transition active:scale-95" title="出題中の自治体にスムーズズーム">
          <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"/></svg>
          <span>フォーカス</span>
        </button>

        <!-- 全体再表示ボタン -->
        <button id="btn-reset-bounds" class="p-2 rounded-lg bg-slate-800/90 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-600/70 shadow-lg backdrop-blur text-xs transition active:scale-95" title="県全体を表示">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/></svg>
        </button>
      </div>

      <!-- ローディングインジケーター -->
      <div id="map-loading-overlay" class="absolute inset-0 bg-slate-900/80 backdrop-blur-sm z-30 flex flex-col items-center justify-center gap-3">
        <div class="w-10 h-10 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
        <div class="text-sm font-semibold text-slate-200">ベクターポリゴン(GeoJSON)を取得中...</div>
        <div id="loading-fallback-msg" class="text-xs text-slate-400 max-w-xs text-center"></div>
      </div>

      <!-- トースト通知 (対象外自治体タップ時の案内) -->
      <div id="map-toast" class="absolute top-14 left-1/2 -translate-x-1/2 z-30 max-w-md bg-slate-900/95 border border-slate-600 text-slate-200 text-xs px-4 py-2.5 rounded-xl shadow-2xl backdrop-blur transition-all duration-300 opacity-0 pointer-events-none translate-y-2 text-center">
        <span id="map-toast-text">通知メッセージ</span>
      </div>

      <!-- 境界線の凡例 (実線＝市境, 点線＝区境) -->
      <div class="absolute bottom-3 left-3 z-10 hidden sm:flex items-center gap-3 bg-slate-900/85 backdrop-blur px-3 py-1.5 rounded-lg border border-slate-700/70 text-[11px] text-slate-300 pointer-events-none shadow-md">
        <span class="flex items-center gap-1.5"><span class="w-4 h-0.5 bg-slate-300 inline-block rounded"></span> 市区町村境</span>
        <span class="flex items-center gap-1.5"><span class="w-4 border-t border-dashed border-slate-400 inline-block"></span> 行政区境</span>
      </div>

      <!-- ========================================== -->
      <!-- 下部操作・回答ドック (モードに応じたUI) -->
      <!-- ========================================== -->
      <div class="absolute bottom-0 left-0 right-0 z-20 p-2 sm:p-4 pointer-events-none">
        <div class="max-w-xl mx-auto pointer-events-auto">

          <!-- モード1: 場所当て (タップ回答) ドック -->
          <div id="dock-locate" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-2xl p-3.5 shadow-2xl">
            <div class="flex items-center justify-between gap-2 mb-2">
              <span id="locate-level-tag" class="text-xs font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full">Level 1 主要都市</span>
              <span id="locate-progress-tag" class="text-xs font-medium text-slate-400">問題 1 / 10</span>
            </div>

            <div class="flex items-center justify-between gap-3">
              <div class="flex-1 min-w-0">
                <div class="text-xs text-slate-400 flex items-center gap-1.5">
                  <span>この自治体を地図上でタップ：</span>
                  <span id="locate-kana" class="text-slate-300 font-medium">（ふりがな）</span>
                </div>
                <div id="locate-question-name" class="text-xl sm:text-2xl font-black text-white truncate tracking-wide">
                  〇〇市
                </div>
              </div>

              <!-- スキップボタン -->
              <button id="btn-locate-skip" class="px-3 py-2 rounded-xl bg-slate-700/70 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white transition active:scale-95 shrink-0">
                スキップ →
              </button>
            </div>

            <!-- フィードバック結果バー (正解/不正解時に出現) -->
            <div id="locate-feedback-bar" class="mt-2.5 pt-2.5 border-t border-slate-700/60 hidden">
              <div id="locate-feedback-content" class="flex items-center justify-between gap-2">
                <!-- JSで動的更新 -->
              </div>
            </div>
          </div>

          <!-- モード2: 名前当て (4択回答) ドック -->
          <div id="dock-name" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-2xl p-3.5 shadow-2xl hidden">
            <div class="flex items-center justify-between gap-2 mb-2">
              <div class="flex items-center gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping"></span>
                <span class="text-xs font-bold text-amber-300">黄色く光っている自治体はどれ？</span>
              </div>
              <span id="name-progress-tag" class="text-xs font-medium text-slate-400">問題 1 / 10</span>
            </div>

            <!-- 4択ボタングリッド -->
            <div class="grid grid-cols-2 gap-2" id="choice-buttons-grid">
              <!-- JSで4つの選択肢ボタンを生成 -->
            </div>
          </div>

          <!-- モード3: エクスプローラー (閲覧・予習) ドック -->
          <div id="dock-explore" class="bg-slate-800/95 backdrop-blur-md border border-slate-700/80 rounded-2xl p-3.5 shadow-2xl hidden">
            <div id="explore-empty-state" class="text-center py-2 text-slate-400 text-xs">
              地図上のポリゴンをタップすると自治体情報が表示されます
            </div>
            <div id="explore-detail-state" class="hidden">
              <div class="flex items-start justify-between gap-2">
                <div>
                  <div class="flex items-center gap-2 mb-0.5">
                    <span id="explore-type-badge" class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">中核市</span>
                    <span id="explore-kana" class="text-xs text-slate-400">はちおうじし</span>
                  </div>
                  <h3 id="explore-name" class="text-lg sm:text-xl font-black text-white">八王子市</h3>
                </div>
                <div class="text-right">
                  <div class="text-[10px] text-slate-400">団体コード (JIS)</div>
                  <div id="explore-code" class="text-xs font-mono font-bold text-slate-200">13201</div>
                </div>
              </div>

              <div class="mt-2.5 pt-2 border-t border-slate-700/60 flex items-center justify-between text-xs">
                <div id="explore-status-tag" class="text-slate-400">未挑戦</div>
                <button id="btn-explore-quiz-this" class="text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1">
                  <span>この自治体をテスト</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- 使い方 & データ管理モーダル -->
  <!-- ========================================== -->
  <div id="modal-help" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 hidden">
    <div class="bg-slate-800 border border-slate-700 rounded-2xl max-w-lg w-full p-5 shadow-2xl max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-3 border-b border-slate-700">
        <h3 class="text-base font-bold text-white flex items-center gap-2">
          <span>📖 GeoAnki 1741 の使い方</span>
        </h3>
        <button id="btn-close-help" class="text-slate-400 hover:text-white p-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <div class="py-4 space-y-4 text-xs sm:text-sm text-slate-300 leading-relaxed">
        <div>
          <h4 class="font-bold text-emerald-400 mb-1">🎯 1,741自治体の定義準拠</h4>
          <p>政令指定都市（20市）の行政区（例：静岡市葵区、駿河区）は市単位に集約して1カウントとし、全国で「792市・743町・183村・23特別区 = 計1,741自治体」として厳密に収録しています。</p>
        </div>

        <div>
          <h4 class="font-bold text-amber-400 mb-1">📶 4段階のステップアップ学習</h4>
          <ul class="list-disc list-inside space-y-0.5 text-slate-400">
            <li><strong class="text-slate-200">Level 1: 主要都市</strong>（県庁所在地・政令市・中核市・特例市）</li>
            <li><strong class="text-slate-200">Level 2: 市・特別区</strong>（Level 1以外の一般市、東京23区）</li>
            <li><strong class="text-slate-200">Level 3: 町</strong>（一般町）</li>
            <li><strong class="text-slate-200">Level 4: 村</strong>（一般村 ※村のない県は自動スキップ）</li>
          </ul>
        </div>

        <div>
          <h4 class="font-bold text-cyan-400 mb-1">🔍 島嶼部・極小エリア救済機能</h4>
          <p>東京都や鹿児島・沖縄などの島嶼部は画面右上のボタンで「本土」「島嶼」を即座に切り替えられます。面積の極めて小さい自治体が出題された時は「フォーカス」アイコンをタップすれば迷子にならずスムーズにズームします。</p>
        </div>

        <div class="pt-3 border-t border-slate-700">
          <div class="flex items-center justify-between">
            <span class="text-slate-400">学習履歴の初期化</span>
            <button id="btn-reset-data" class="px-3 py-1.5 rounded-lg bg-rose-950 text-rose-300 border border-rose-800 hover:bg-rose-900 text-xs font-semibold transition">
              履歴を全リセット
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- 埋め込みデータ & アプリケーションスクリプト -->
  <!-- ========================================== -->
  <script>
    // 1. 都道府県マスター
    const PREFECTURES = {pref_json_str};

    // 2. 政令指定都市行政区マッピング (185行政区 -> 親市コード)
    const WARD_TO_CITY = {ward_json_str};

    // 3. 全国1,741自治体マスターデータ [c, p, pref, n, k, t, lvl, lat, lng]
    const RAW_MUNICIPALITIES = {muni_json_str};

    // 高速ルックアップ用マップの構築
    const MUNICIPALITIES = {{}};
    const PREF_MUNICIPALITIES = {{}}; // prefCode -> [muni]

    RAW_MUNICIPALITIES.forEach(([c, p, pref, n, k, t, lvl, lat, lng]) => {{
      const item = {{ c, p, pref, n, k, t, lvl, lat, lng }};
      MUNICIPALITIES[c] = item;
      if (!PREF_MUNICIPALITIES[p]) PREF_MUNICIPALITIES[p] = [];
      PREF_MUNICIPALITIES[p].push(item);
    }});

    // 種別ラベル
    const TYPE_LABELS = {{
      'designated': '政令指定都市',
      'capital': '県庁所在地',
      'core': '中核市',
      'special': '特例市',
      'major': '主要都市',
      'city_all': '市',
      'city': '一般市',
      'ward': '特別区',
      'town': '町',
      'village': '村'
    }};
  </script>

  <!-- アプリケーション本体スクリプト -->
  <script>
    /* ========================================================
       Web Audio API による効果音エンジン（外部通信なし）
       ======================================================== */
    class SoundEngine {{
      constructor() {{
        this.ctx = null;
        this.enabled = true;
      }}
      init() {{
        if (!this.ctx) {{
          const AudioCtx = window.AudioContext || window.webkitAudioContext;
          if (AudioCtx) this.ctx = new AudioCtx();
        }}
        if (this.ctx && this.ctx.state === 'suspended') {{
          this.ctx.resume();
        }}
      }}
      playCorrect() {{
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, now); // D5
        osc.frequency.setValueAtTime(880.00, now + 0.1); // A5
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.35);
      }}
      playWrong() {{
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.setValueAtTime(174.61, now + 0.1);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.35);
      }}
    }}
    const sound = new SoundEngine();

    /* ========================================================
       ローカルストレージ管理 (学習履歴 & 制覇状況)
       ======================================================== */
    const STORAGE_KEY = 'geoanki_muni_v1';
    class Store {{
      static load() {{
        try {{
          const raw = localStorage.getItem(STORAGE_KEY);
          return raw ? JSON.parse(raw) : {{ records: {{}}, sound: true }};
        }} catch(e) {{
          return {{ records: {{}}, sound: true }};
        }}
      }}
      static save(data) {{
        try {{
          localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        }} catch(e) {{}}
      }}
      static recordAnswer(code, isCorrect) {{
        const data = this.load();
        if (!data.records[code]) {{
          data.records[code] = {{ correct: 0, wrong: 0, last: null, updated: Date.now() }};
        }}
        const r = data.records[code];
        if (isCorrect) {{
          r.correct += 1;
          r.last = 'correct';
        }} else {{
          r.wrong += 1;
          r.last = 'wrong';
        }}
        r.updated = Date.now();
        this.save(data);
      }}
      static getRecord(code) {{
        const data = this.load();
        return data.records[code] || null;
      }}
      static getPrefClearedCount(prefCode) {{
        const data = this.load();
        const list = PREF_MUNICIPALITIES[prefCode] || [];
        let count = 0;
        list.forEach(m => {{
          const r = data.records[m.c];
          if (r && r.correct > 0) count++;
        }});
        return count;
      }}
      static getTotalClearedCount() {{
        const data = this.load();
        let count = 0;
        Object.keys(data.records).forEach(code => {{
          if (MUNICIPALITIES[code] && data.records[code].correct > 0) {{
            count++;
          }}
        }});
        return count;
      }}
      static getWeakList(prefCode) {{
        const data = this.load();
        const list = PREF_MUNICIPALITIES[prefCode] || [];
        return list.filter(m => {{
          const r = data.records[m.c];
          return r && (r.wrong > 0 && r.last === 'wrong');
        }});
      }}
      static resetAll() {{
        localStorage.removeItem(STORAGE_KEY);
      }}
    }}

    /* ========================================================
       アプリケーション状態管理
       ======================================================== */
    const state = {{
      currentScreen: 'hub', // 'hub' | 'spoke'
      selectedPref: null, // pref object
      selectedLevel: '1', // '1' | '2' | '3' | '4' | 'ALL' | 'WEAK'
      currentMode: 'locate', // 'locate' | 'name' | 'explore'
      activeQuestionList: [],
      currentIndex: 0,
      currentQuestion: null,
      currentChoices: [],
      map: null,
      geoJsonLayer: null,
      cityLayerMap: {{}}, // code -> [Leaflet layer]
      cityBorderLayers: {{}}, // parentCityCode -> outer border Leaflet layer
      isAnswering: false,
      feedbackTimer: null,
      loadedGeoJsonCache: {{}} // prefCode -> geojson
    }};

    /* ========================================================
       Hub (都道府県セレクト画面) ロジック
       ======================================================== */
    function initHub() {{
      renderHubSummary();
      renderPrefGrid('ALL');

      // 地方フィルターボタン
      document.querySelectorAll('.region-filter-btn').forEach(btn => {{
        btn.addEventListener('click', (e) => {{
          document.querySelectorAll('.region-filter-btn').forEach(b => {{
            b.classList.remove('bg-emerald-500', 'text-white');
            b.classList.add('bg-slate-800', 'text-slate-300');
          }});
          btn.classList.add('bg-emerald-500', 'text-white');
          btn.classList.remove('bg-slate-800', 'text-slate-300');
          renderPrefGrid(btn.dataset.region);
        }});
      }});

      // ヘルプモーダル
      const modal = document.getElementById('modal-help');
      document.getElementById('btn-show-help').onclick = () => modal.classList.remove('hidden');
      document.getElementById('btn-close-help').onclick = () => modal.classList.add('hidden');
      modal.onclick = (e) => {{ if (e.target === modal) modal.classList.add('hidden'); }};

      // データリセットボタン
      document.getElementById('btn-reset-data').onclick = () => {{
        if (confirm('すべての正答履歴・制覇記録をリセットしますか？この操作は取り消せません。')) {{
          Store.resetAll();
          modal.classList.add('hidden');
          renderHubSummary();
          renderPrefGrid('ALL');
        }}
      }};
    }}

    function renderHubSummary() {{
      const cleared = Store.getTotalClearedCount();
      const total = 1741;
      const pct = ((cleared / total) * 100).toFixed(1);

      document.getElementById('hub-total-cleared').textContent = cleared.toLocaleString();
      document.getElementById('hub-total-pct').textContent = `(${{pct}}%)`;
      document.getElementById('hub-progress-bar').style.width = `${{pct}}%`;

      let compCount = 0;
      PREFECTURES.forEach(p => {{
        const pTotal = (PREF_MUNICIPALITIES[p.code] || []).length;
        const pCleared = Store.getPrefClearedCount(p.code);
        if (pTotal > 0 && pCleared === pTotal) compCount++;
      }});
      document.getElementById('hub-pref-completed-count').textContent = compCount;
    }}

    function renderPrefGrid(selectedRegion) {{
      const container = document.getElementById('hub-pref-container');
      container.innerHTML = '';

      // 地方ごとにグルーピング
      const regionMap = {{}};
      PREFECTURES.forEach(p => {{
        if (selectedRegion !== 'ALL' && p.region !== selectedRegion) return;
        if (!regionMap[p.region]) regionMap[p.region] = [];
        regionMap[p.region].push(p);
      }});

      Object.entries(regionMap).forEach(([region, prefs]) => {{
        const section = document.createElement('div');
        section.className = 'space-y-2.5';

        const title = document.createElement('h3');
        title.className = 'text-xs font-bold text-slate-400 tracking-wider uppercase flex items-center gap-2';
        title.innerHTML = `<span>${{region}}</span><span class="h-px flex-1 bg-slate-800"></span>`;
        section.appendChild(title);

        const grid = document.createElement('div');
        grid.className = 'grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2.5';

        prefs.forEach(p => {{
          const list = PREF_MUNICIPALITIES[p.code] || [];
          const total = list.length;
          const cleared = Store.getPrefClearedCount(p.code);
          const pct = total > 0 ? Math.round((cleared / total) * 100) : 0;
          const isComplete = total > 0 && cleared === total;

          const card = document.createElement('div');
          card.className = `p-3 rounded-xl border transition cursor-pointer select-none relative overflow-hidden group hover:scale-[1.02] active:scale-[0.98] ${{
            isComplete
              ? 'bg-gradient-to-b from-emerald-950/40 to-slate-800 border-emerald-500/50 hover:border-emerald-400'
              : cleared > 0
                ? 'bg-slate-800/90 border-slate-700 hover:border-slate-500'
                : 'bg-slate-800/50 border-slate-700/50 hover:border-slate-600'
          }}`;

          card.innerHTML = `
            <div class="flex items-center justify-between gap-1 mb-1.5">
              <span class="text-sm sm:text-base font-bold text-white group-hover:text-emerald-400 transition">${{p.name}}</span>
              ${{isComplete 
                ? '<span class="text-[10px] font-black px-1.5 py-0.5 rounded bg-emerald-500 text-slate-950">CLEAR</span>'
                : cleared > 0 
                  ? `<span class="text-[10px] font-semibold text-emerald-400">${{pct}}%</span>`
                  : '<span class="text-[10px] text-slate-500">未挑戦</span>'
              }}
            </div>
            <div class="text-[11px] text-slate-400 mb-2">
              <span class="font-semibold text-slate-200">${{cleared}}</span> / ${{total}} 自治体
            </div>
            <div class="w-full bg-slate-700/60 h-1.5 rounded-full overflow-hidden">
              <div class="bg-emerald-400 h-full rounded-full transition-all" style="width: ${{pct}}%"></div>
            </div>
          `;

          card.onclick = () => openPrefecture(p.code);
          grid.appendChild(card);
        }});

        section.appendChild(grid);
        container.appendChild(section);
      }});
    }}

    /* ========================================================
       Spoke (都道府県別学習画面) 遷移・初期化
       ======================================================== */
    function openPrefecture(prefCode) {{
      const pref = PREFECTURES.find(p => p.code === prefCode);
      if (!pref) return;

      state.selectedPref = pref;
      state.currentScreen = 'spoke';

      // 画面切り替え
      document.getElementById('screen-hub').classList.add('hidden');
      document.getElementById('screen-spoke').classList.remove('hidden');

      // ヘッダー情報更新
      document.getElementById('spoke-pref-name').textContent = pref.name;
      const list = PREF_MUNICIPALITIES[prefCode] || [];
      document.getElementById('spoke-pref-count-badge').textContent = `${{list.length}}自治体`;

      updateSpokeHeaderProgress();

      // 島嶼部ボタンの生成
      setupIslandButtons(pref);

      // 地図初期化
      setupMap();

      // GeoJSON のオンデマンド読み込み
      loadPrefGeoJson(prefCode);
    }}

    function updateSpokeHeaderProgress() {{
      const prefCode = state.selectedPref.code;
      const list = PREF_MUNICIPALITIES[prefCode] || [];
      const cleared = Store.getPrefClearedCount(prefCode);
      const total = list.length;
      const pct = total > 0 ? Math.round((cleared / total) * 100) : 0;

      document.getElementById('spoke-cleared-count').textContent = cleared;
      document.getElementById('spoke-total-count').textContent = total;
      document.getElementById('spoke-cleared-pct').textContent = `(${{pct}}%)`;
    }}

    function setupIslandButtons(pref) {{
      const container = document.getElementById('island-buttons-container');
      container.innerHTML = '';
      if (!pref.islands || pref.islands.length === 0) return;

      const group = document.createElement('div');
      group.className = 'flex flex-col gap-1 bg-slate-800/90 p-1 rounded-xl border border-slate-700/80 shadow-lg backdrop-blur';

      pref.islands.forEach(island => {{
        const btn = document.createElement('button');
        btn.className = 'px-2.5 py-1 rounded-lg text-xs font-semibold text-slate-200 hover:text-white hover:bg-slate-700 transition active:scale-95 text-left';
        btn.innerHTML = `📍 ${{island.label}}`;
        btn.onclick = () => {{
          if (state.map) {{
            const targetBounds = (island.label === '全域' && state.geoJsonLayer)
              ? state.geoJsonLayer.getBounds()
              : L.latLngBounds(island.bounds);
            state.map.fitBounds(targetBounds, {{
              paddingTopLeft: [20, 20],
              paddingBottomRight: [20, window.innerWidth < 640 ? 190 : 140],
              maxZoom: 11
            }});
          }}
        }};
        group.appendChild(btn);
      }});

      container.appendChild(group);
    }}

    function setupMap() {{
      if (state.map) {{
        state.map.invalidateSize();
        return;
      }}

      // Leaflet 地図インスタンス初期化
      // 外部タイルサーバーを使わない完全無地ベクターマップ（ウォーターマークなし）
      state.map = L.map('map', {{
        zoomControl: false,
        attributionControl: false,
        minZoom: 4,
        maxZoom: 16
      }}).setView([36.5, 138.0], 7);

      // ズームコントロールを右上に配置
      L.control.zoom({{ position: 'topright' }}).addTo(state.map);

      // 画面リサイズ・回転時の自動再センタリング
      let resizeTimer = null;
      window.addEventListener('resize', () => {{
        if (state.currentScreen !== 'spoke' || !state.map) return;
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {{
          state.map.invalidateSize();
          if (state.geoJsonLayer) {{
            fitMapToBounds(state.geoJsonLayer.getBounds());
          }}
        }}, 200);
      }});
    }}

    function fitMapToBounds(bounds) {{
      if (!state.map || !bounds.isValid()) return;
      const isMobile = window.innerWidth < 640;
      state.map.fitBounds(bounds, {{
        paddingTopLeft: [20, 20],
        paddingBottomRight: [20, isMobile ? 220 : 160],
        maxZoom: 12
      }});
    }}

    /* ========================================================
       GeoJSON オンデマンド読み込み & セルフバリデーション
       ======================================================== */
    async function loadPrefGeoJson(prefCode) {{
      const loading = document.getElementById('map-loading-overlay');
      const fallbackMsg = document.getElementById('loading-fallback-msg');
      loading.classList.remove('hidden');
      fallbackMsg.textContent = '';

      // 既存レイヤーのクリア
      if (state.geoJsonLayer && state.map) {{
        state.map.removeLayer(state.geoJsonLayer);
        state.geoJsonLayer = null;
      }}
      if (state.cityBorderLayers) {{
        Object.values(state.cityBorderLayers).forEach(l => state.map.removeLayer(l));
      }}
      state.cityBorderLayers = {{}};
      state.cityLayerMap = {{}};

      let geoData = state.loadedGeoJsonCache[prefCode];

      if (!geoData) {{
        const primaryUrl = `https://cdn.jsdelivr.net/gh/smartnews-smri/japan-topography@main/data/municipality/geojson/s0010/N03-21_${{prefCode}}_210101.json`;
        const fallbackUrl = `https://raw.githubusercontent.com/smartnews-smri/japan-topography/main/data/municipality/geojson/s0010/N03-21_${{prefCode}}_210101.json`;

        try {{
          const res = await fetch(primaryUrl);
          if (!res.ok) throw new Error(`HTTP ${{res.status}}`);
          geoData = await res.json();
        }} catch(e) {{
          console.warn('jsDelivr failed, trying GitHub raw fallback...', e);
          fallbackMsg.textContent = 'バックアップCDNから取得中...';
          try {{
            const res2 = await fetch(fallbackUrl);
            if (!res2.ok) throw new Error(`Fallback HTTP ${{res2.status}}`);
            geoData = await res2.json();
          }} catch(e2) {{
            console.error('All GeoJSON fetch attempts failed', e2);
            alert('地図データの読み込みに失敗しました。インターネット接続を確認して再読み込みしてください。');
            loading.classList.add('hidden');
            return;
          }}
        }}
        state.loadedGeoJsonCache[prefCode] = geoData;
      }}

      // セルフバリデーション実行
      runSelfValidation(prefCode, geoData);

      // GeoJSON レイヤーの生成 & ポリゴンスタイリング
      renderGeoJsonLayer(geoData);

      loading.classList.add('hidden');

      // Levelタブの件数更新 & 適切なLevelを選択
      setupLevelTabs();

      // 出題リスト構築 & 開始
      initStage();
    }}

    // セルフバリデーション機構 (コンソール健全性チェック)
    function runSelfValidation(prefCode, geoData) {{
      const missingInMaster = [];
      const geoCityCodes = new Set();

      (geoData.features || []).forEach(f => {{
        const rawCode = f.properties.N03_007;
        const mappedCode = WARD_TO_CITY[rawCode] || rawCode;
        geoCityCodes.add(mappedCode);

        if (!MUNICIPALITIES[mappedCode]) {{
          missingInMaster.push({{ raw: rawCode, mapped: mappedCode, name: f.properties.N03_004 }});
        }}
      }});

      const defMunis = PREF_MUNICIPALITIES[prefCode] || [];
      const missingInGeo = defMunis.filter(m => !geoCityCodes.has(m.c));

      if (missingInGeo.length > 0) {{
        console.warn(`[GeoAnki Self-Validation Alert] 都道府県 ${{prefCode}}: GeoJSON側欠損 ${{missingInGeo.length}}件`, {{
          missingInMaster,
          missingInGeo
        }});
      }} else {{
        console.log(`[GeoAnki Self-Validation Passed] 都道府県 ${{prefCode}}: 全${{defMunis.length}}自治体が完全整合`);
      }}
    }}

    /* ========================================================
       難易度Level判定 & 動的ポリゴンスタイリング（市境 vs 区境の分離）
       ======================================================== */
    function isMuniTargetInCurrentStage(code) {{
      const muni = MUNICIPALITIES[code];
      if (!muni) return false;
      // 探索モードまたは「全自治体」タブの場合は全自治体が対象
      if (state.currentMode === 'explore' || state.selectedLevel === 'ALL') {{
        return true;
      }}
      // 弱点復習タブの場合
      if (state.selectedLevel === 'WEAK') {{
        const rec = Store.getRecord(code);
        return rec && rec.wrong > 0 && rec.last === 'wrong';
      }}
      // Level 1〜4の場合
      return muni.lvl === parseInt(state.selectedLevel, 10);
    }}

    // Turf.js を利用した政令市の行政区結合
    function mergeFeaturesForCity(features) {{
      if (!window.turf || !features || features.length === 0) return null;
      if (features.length === 1) return features[0];
      try {{
        let merged = features[0];
        for (let i = 1; i < features.length; i++) {{
          merged = turf.union(merged, features[i]);
        }}
        return merged;
      }} catch (err) {{
        console.warn('[Turf Union] Fallback:', err);
        return null;
      }}
    }}

    function getCityNormalStyle(code, isWard) {{
      const isTarget = isMuniTargetInCurrentStage(code);
      const dash = isWard ? '3, 4' : null;
      const baseWeight = isWard ? 1.0 : 1.8;

      // 出題対象外の自治体: 海と明瞭に区別できるスレートグレー
      if (!isTarget) {{
        return {{
          fillColor: '#334155',
          fillOpacity: 0.70,
          color: isWard ? '#64748b' : '#475569',
          weight: isWard ? 0.9 : 1.3,
          dashArray: dash,
          opacity: 0.85
        }};
      }}

      // 出題対象自治体: 過去にクリア済み
      const rec = Store.getRecord(code);
      if (rec && rec.correct > 0) {{
        return {{
          fillColor: '#ecfdf5',
          fillOpacity: 0.92,
          color: isWard ? '#a7f3d0' : '#34d399',
          weight: baseWeight,
          dashArray: dash,
          opacity: 1
        }};
      }}

      // 出題対象自治体: 未クリア（クリアな白〜極薄グレー）
      return {{
        fillColor: '#f8fafc',
        fillOpacity: 0.95,
        color: isWard ? '#94a3b8' : '#64748b',
        weight: baseWeight,
        dashArray: dash,
        opacity: 1
      }};
    }}

    // 政令指定都市の「太い外周枠線（市境）」スタイル
    function getCityOuterBorderStyle(code) {{
      const isTarget = isMuniTargetInCurrentStage(code);
      if (!isTarget) {{
        return {{
          fill: false,
          color: '#64748b',
          weight: 1.8,
          opacity: 0.85
        }};
      }}
      const rec = Store.getRecord(code);
      if (rec && rec.correct > 0) {{
        return {{
          fill: false,
          color: '#059669',
          weight: 2.4,
          opacity: 1
        }};
      }}
      return {{
        fill: false,
        color: '#475569',
        weight: 2.2,
        opacity: 1
      }};
    }}

    // 地図ポリゴン描画（2層レイヤー構造: 下層=行政区破線 / 上層=政令市外郭実線）
    function renderGeoJsonLayer(geoData) {{
      state.geoJsonLayer = L.geoJSON(geoData, {{
        style: (feature) => {{
          const rawCode = feature.properties.N03_007;
          const code = WARD_TO_CITY[rawCode] || rawCode;
          const isWard = !!WARD_TO_CITY[rawCode];
          return getCityNormalStyle(code, isWard);
        }},
        onEachFeature: (feature, layer) => {{
          const rawCode = feature.properties.N03_007;
          const code = WARD_TO_CITY[rawCode] || rawCode;
          const isWard = !!WARD_TO_CITY[rawCode];
          layer._isWard = isWard;
          layer._cityCode = code;

          if (!state.cityLayerMap[code]) {{
            state.cityLayerMap[code] = [];
          }}
          state.cityLayerMap[code].push(layer);

          // ホバー・クリックイベント
          layer.on({{
            mouseover: () => {{
              if (isMuniTargetInCurrentStage(code) || state.currentMode === 'explore') {{
                highlightCity(code, 'hover');
              }}
            }},
            mouseout: () => {{
              resetCityHighlight(code);
            }},
            click: (e) => {{
              L.DomEvent.stopPropagation(e);
              handlePolygonClick(code);
            }}
          }});
        }}
      }}).addTo(state.map);

      // 政令指定都市の全区ポリゴンをマージして親市の外郭（太い実線市境）を上層オーバーレイ
      const designatedCityFeatures = {{}};
      (geoData.features || []).forEach(f => {{
        const rawCode = f.properties.N03_007;
        const parentCity = WARD_TO_CITY[rawCode];
        if (parentCity) {{
          if (!designatedCityFeatures[parentCity]) designatedCityFeatures[parentCity] = [];
          designatedCityFeatures[parentCity].push(f);
        }}
      }});

      Object.entries(designatedCityFeatures).forEach(([cityCode, featList]) => {{
        const merged = mergeFeaturesForCity(featList);
        if (merged) {{
          const outerLayer = L.geoJSON(merged, {{
            style: () => getCityOuterBorderStyle(cityCode),
            interactive: false
          }}).addTo(state.map);
          state.cityBorderLayers[cityCode] = outerLayer;
        }}
      }});

      // 初回表示フィット（本土・本島の defaultView があれば優先）
      if (state.selectedPref && state.selectedPref.defaultView) {{
        fitMapToBounds(L.latLngBounds(state.selectedPref.defaultView));
      }} else {{
        fitMapToBounds(state.geoJsonLayer.getBounds());
      }}
    }}

    // ポリゴンハイライト制御
    function setCityStyle(code, styleObj) {{
      const layers = state.cityLayerMap[code];
      if (!layers) return;
      layers.forEach(l => l.setStyle(styleObj));
    }}

    function highlightCity(code, mode) {{
      const layers = state.cityLayerMap[code];
      if (!layers) return;

      layers.forEach(l => {{
        const isWard = l._isWard;
        const dash = isWard ? '3, 4' : null;

        if (mode === 'question') {{
          l.setStyle({{
            fillColor: '#fde047',
            fillOpacity: 0.95,
            color: '#ca8a04',
            weight: isWard ? 1.4 : 3.2,
            dashArray: dash,
            opacity: 1
          }});
        }} else if (mode === 'correct') {{
          l.setStyle({{
            fillColor: '#34d399',
            fillOpacity: 0.95,
            color: '#059669',
            weight: isWard ? 1.4 : 2.8,
            dashArray: dash,
            opacity: 1
          }});
        }} else if (mode === 'wrong') {{
          l.setStyle({{
            fillColor: '#f87171',
            fillOpacity: 0.95,
            color: '#dc2626',
            weight: isWard ? 1.4 : 2.8,
            dashArray: dash,
            opacity: 1
          }});
        }} else if (mode === 'hover') {{
          if (state.currentQuestion && state.currentQuestion.c === code) return;
          l.setStyle({{
            fillColor: '#e2e8f0',
            weight: isWard ? 1.2 : 2.2,
            dashArray: dash,
            opacity: 1
          }});
        }}
      }});

      // 親市外郭レイヤー（太い実線市境）も連動ハイライト
      const borderLayer = state.cityBorderLayers[code];
      if (borderLayer) {{
        if (mode === 'question') {{
          borderLayer.setStyle({{ color: '#ca8a04', weight: 3.8, opacity: 1 }});
        }} else if (mode === 'correct') {{
          borderLayer.setStyle({{ color: '#059669', weight: 3.0, opacity: 1 }});
        }} else if (mode === 'wrong') {{
          borderLayer.setStyle({{ color: '#dc2626', weight: 3.0, opacity: 1 }});
        }} else if (mode === 'hover') {{
          if (state.currentQuestion && state.currentQuestion.c === code) return;
          borderLayer.setStyle({{ color: '#94a3b8', weight: 2.6, opacity: 1 }});
        }}
      }}
    }}

    function resetCityHighlight(code) {{
      const layers = state.cityLayerMap[code];
      if (layers) {{
        layers.forEach(l => {{
          l.setStyle(getCityNormalStyle(code, l._isWard));
        }});
      }}
      const borderLayer = state.cityBorderLayers[code];
      if (borderLayer) {{
        borderLayer.setStyle(getCityOuterBorderStyle(code));
      }}
    }}

    function refreshAllCityStyles() {{
      if (!state.geoJsonLayer) return;
      Object.keys(state.cityLayerMap).forEach(code => {{
        resetCityHighlight(code);
      }});
    }}

    // 親切なトースト通知
    let toastTimer = null;
    function showToast(msg) {{
      const toast = document.getElementById('map-toast');
      const text = document.getElementById('map-toast-text');
      if (!toast || !text) return;
      text.textContent = msg;
      toast.classList.remove('opacity-0', 'translate-y-2', 'pointer-events-none');
      toast.classList.add('opacity-100', 'translate-y-0');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {{
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', 'translate-y-2', 'pointer-events-none');
      }}, 2600);
    }}

    /* ========================================================
       Level タブ & 出題ステージ制御 (例外処理・動的昇格・0件除外)
       ======================================================== */
    function setupLevelTabs() {{
      const prefCode = state.selectedPref.code;
      const allMunis = PREF_MUNICIPALITIES[prefCode] || [];

      const counts = {{ '1': 0, '2': 0, '3': 0, '4': 0, 'ALL': allMunis.length }};
      allMunis.forEach(m => {{
        if (counts[m.lvl] !== undefined) counts[m.lvl]++;
      }});

      const weakList = Store.getWeakList(prefCode);
      const isTokyo = prefCode === '13';
      const isSmallCityPref = counts['2'] === 0 && counts['1'] > 0;

      // 各タブの表示・非表示と動的ラベル
      document.querySelectorAll('.level-tab-btn').forEach(btn => {{
        const lvl = btn.dataset.level;
        const textSpan = btn.querySelector('.tab-label');
        const countSpan = btn.querySelector('.tab-count');

        if (lvl === 'WEAK') {{
          countSpan.textContent = `(${{weakList.length}})`;
          if (weakList.length > 0) {{
            btn.classList.remove('hidden');
          }} else {{
            btn.classList.add('hidden');
          }}
        }} else if (lvl === 'ALL') {{
          countSpan.textContent = `(${{counts['ALL']}})`;
          btn.classList.remove('hidden');
        }} else {{
          const count = counts[lvl] || 0;
          countSpan.textContent = `(${{count}})`;

          // ルール2: 0件ステージの完全非表示（村なし県、統合されたLevel 2など）
          if (count === 0) {{
            btn.classList.add('hidden');
          }} else {{
            btn.classList.remove('hidden');
            // ラベルの動的カスタマイズ
            if (lvl === '1') {{
              if (isTokyo) textSpan.textContent = 'Lv.1 特別区';
              else if (isSmallCityPref) textSpan.textContent = 'Lv.1 市全域';
              else textSpan.textContent = 'Lv.1 主要都市';
            }} else if (lvl === '2') {{
              if (isTokyo) textSpan.textContent = 'Lv.2 市(多摩)';
              else textSpan.textContent = 'Lv.2 市';
            }} else if (lvl === '3') {{
              textSpan.textContent = 'Lv.3 町';
            }} else if (lvl === '4') {{
              textSpan.textContent = 'Lv.4 村';
            }}
          }}
        }}
      }});

      // 初期Level選択: 選択中のLevelが非表示（0件）になっている場合、利用可能な最初のLevelを選択
      if (state.selectedLevel !== 'ALL' && state.selectedLevel !== 'WEAK') {{
        if (counts[state.selectedLevel] === 0) {{
          if (counts['1'] > 0) state.selectedLevel = '1';
          else if (counts['2'] > 0) state.selectedLevel = '2';
          else if (counts['3'] > 0) state.selectedLevel = '3';
          else if (counts['4'] > 0) state.selectedLevel = '4';
          else state.selectedLevel = 'ALL';
        }}
      }}

      updateLevelTabStyles();
    }}

    function updateLevelTabStyles() {{
      document.querySelectorAll('.level-tab-btn').forEach(btn => {{
        const lvl = btn.dataset.level;
        if (lvl === state.selectedLevel) {{
          btn.classList.add('bg-emerald-500', 'text-white', 'font-semibold');
          btn.classList.remove('bg-slate-800', 'text-slate-300');
        }} else {{
          btn.classList.remove('bg-emerald-500', 'text-white', 'font-semibold');
          btn.classList.add('bg-slate-800', 'text-slate-300');
        }}
      }});
    }}

    // タブクリックイベント登録
    document.addEventListener('DOMContentLoaded', () => {{
      document.querySelectorAll('.level-tab-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          state.selectedLevel = btn.dataset.level;
          updateLevelTabStyles();
          initStage();
        }});
      }});

      document.querySelectorAll('.mode-tab-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          document.querySelectorAll('.mode-tab-btn').forEach(b => {{
            b.classList.remove('bg-slate-700', 'text-emerald-400', 'shadow', 'font-semibold');
            b.classList.add('text-slate-300', 'font-medium');
          }});
          btn.classList.add('bg-slate-700', 'text-emerald-400', 'shadow', 'font-semibold');
          btn.classList.remove('text-slate-300', 'font-medium');

          state.currentMode = btn.dataset.mode;
          switchModeUI();
          initStage();
        }});
      }});

      // 戻るボタン
      document.getElementById('btn-back-hub').onclick = () => {{
        state.currentScreen = 'hub';
        document.getElementById('screen-spoke').classList.add('hidden');
        document.getElementById('screen-hub').classList.remove('hidden');
        renderHubSummary();
        renderPrefGrid('ALL');
      }};

      // 音声ON/OFF
      const btnSound = document.getElementById('btn-toggle-sound');
      const iconOn = document.getElementById('icon-sound-on');
      const iconOff = document.getElementById('icon-sound-off');
      btnSound.onclick = () => {{
        sound.enabled = !sound.enabled;
        iconOn.classList.toggle('hidden', !sound.enabled);
        iconOff.classList.toggle('hidden', sound.enabled);
      }};

      // 虫眼鏡（フォーカス）ボタン
      document.getElementById('btn-focus-current').onclick = () => {{
        focusCurrentMunicipality();
      }};

      // 本土・全体再表示ボタン
      document.getElementById('btn-reset-bounds').onclick = () => {{
        if (state.selectedPref && state.selectedPref.defaultView) {{
          fitMapToBounds(L.latLngBounds(state.selectedPref.defaultView));
        }} else if (state.geoJsonLayer) {{
          fitMapToBounds(state.geoJsonLayer.getBounds());
        }}
      }};

      // スキップボタン
      document.getElementById('btn-locate-skip').onclick = () => {{
        nextQuestion();
      }};
    }});

    function switchModeUI() {{
      document.getElementById('dock-locate').classList.toggle('hidden', state.currentMode !== 'locate');
      document.getElementById('dock-name').classList.toggle('hidden', state.currentMode !== 'name');
      document.getElementById('dock-explore').classList.toggle('hidden', state.currentMode !== 'explore');

      const btnFocus = document.getElementById('btn-focus-current');
      btnFocus.classList.toggle('hidden', state.currentMode === 'explore');
    }}

    function initStage() {{
      const prefCode = state.selectedPref.code;
      const allMunis = PREF_MUNICIPALITIES[prefCode] || [];

      let list = [];
      if (state.selectedLevel === 'ALL') {{
        list = [...allMunis];
      }} else if (state.selectedLevel === 'WEAK') {{
        list = Store.getWeakList(prefCode);
      }} else {{
        const targetLvl = parseInt(state.selectedLevel, 10);
        list = allMunis.filter(m => m.lvl === targetLvl);
      }}

      // シャッフル（未正解の自治体を優先して手前に配置）
      const storeData = Store.load();
      list.sort((a, b) => {{
        const recA = storeData.records[a.c];
        const recB = storeData.records[b.c];
        const clearedA = recA && recA.correct > 0 ? 1 : 0;
        const clearedB = recB && recB.correct > 0 ? 1 : 0;
        if (clearedA !== clearedB) return clearedA - clearedB;
        return Math.random() - 0.5;
      }});

      state.activeQuestionList = list;
      state.currentIndex = 0;
      state.isAnswering = false;

      // 現在のLevelに応じて全ポリゴンのスタイル（対象/グレーアウト）を同期
      refreshAllCityStyles();

      if (state.currentMode === 'explore') {{
        // エクスプローラーモード: クイズなし
        document.getElementById('explore-empty-state').classList.remove('hidden');
        document.getElementById('explore-detail-state').classList.add('hidden');
      }} else {{
        loadQuestion();
      }}
    }}

    function loadQuestion() {{
      if (state.activeQuestionList.length === 0) {{
        if (state.selectedLevel === 'WEAK') {{
          alert('弱点復習リストの自治体は現在ありません！すべて克服しました。');
          state.selectedLevel = 'ALL';
          updateLevelTabStyles();
          initStage();
        }} else {{
          alert('このカテゴリの自治体は現在ありません。');
        }}
        return;
      }}

      if (state.currentIndex >= state.activeQuestionList.length) {{
        // ステージ完了！
        sound.playCorrect();
        alert(`🎉 ステージクリア！ 全${{state.activeQuestionList.length}}問の学習を達成しました！`);
        updateSpokeHeaderProgress();
        setupLevelTabs();
        initStage();
        return;
      }}

      // 前回のハイライト解除
      if (state.currentQuestion) {{
        resetCityHighlight(state.currentQuestion.c);
      }}

      state.currentQuestion = state.activeQuestionList[state.currentIndex];
      state.isAnswering = false;

      const q = state.currentQuestion;
      const totalQ = state.activeQuestionList.length;
      const currentNum = state.currentIndex + 1;

      if (state.currentMode === 'locate') {{
        // 場所当てモード
        let lvlLabel = `Lv.${{q.lvl}}`;
        if (state.selectedPref.code === '13') {{
          if (q.lvl === 1) lvlLabel = '特別区';
          else if (q.lvl === 2) lvlLabel = '市(多摩)';
          else if (q.lvl === 3) lvlLabel = '町';
          else if (q.lvl === 4) lvlLabel = '村';
        }} else if (q.t === 'city_all') {{
          lvlLabel = '市(全域)';
        }} else {{
          lvlLabel = `Lv.${{q.lvl}} ${{TYPE_LABELS[q.t] || '市町村'}}`;
        }}
        document.getElementById('locate-level-tag').textContent = lvlLabel;
        document.getElementById('locate-progress-tag').textContent = `問 ${{currentNum}} / ${{totalQ}}`;
        document.getElementById('locate-question-name').textContent = q.n;
        document.getElementById('locate-kana').textContent = `（${{q.k}}）`;

        const feedbackBar = document.getElementById('locate-feedback-bar');
        feedbackBar.classList.add('hidden');
      }} else if (state.currentMode === 'name') {{
        // 名前当てモード: 地図上のポリゴンをイエローハイライト
        document.getElementById('name-progress-tag').textContent = `問 ${{currentNum}} / ${{totalQ}}`;
        highlightCity(q.c, 'question');

        // 4択ボタンの生成
        generateChoices(q);
      }}

      // 出題自治体が現在の地図表示範囲外にある場合、自動で該当エリアへスムーズズーム
      if (state.map && state.cityLayerMap[q.c] && state.cityLayerMap[q.c].length > 0) {{
        const qGroup = L.featureGroup(state.cityLayerMap[q.c]);
        const qCenter = qGroup.getBounds().getCenter();
        if (!state.map.getBounds().contains(qCenter)) {{
          state.map.flyToBounds(qGroup.getBounds(), {{
            padding: [60, 60],
            maxZoom: 11,
            duration: 0.8
          }});
        }}
      }}
    }}

    function focusCurrentMunicipality() {{
      if (!state.currentQuestion || !state.map) return;
      const layers = state.cityLayerMap[state.currentQuestion.c];
      if (layers && layers.length > 0) {{
        const group = L.featureGroup(layers);
        state.map.flyToBounds(group.getBounds(), {{
          padding: [50, 50],
          maxZoom: 13,
          duration: 0.8
        }});
      }}
    }}

    /* ========================================================
       名前当てモード: 4択生成 & 回答処理
       ======================================================== */
    function generateChoices(targetMuni) {{
      const prefCode = state.selectedPref.code;
      const allMunis = PREF_MUNICIPALITIES[prefCode] || [];

      // ダミー選択肢（現在のステージ対象自治体から優先抽出）
      let targetCandidates = state.activeQuestionList.filter(m => m.c !== targetMuni.c);
      if (targetCandidates.length < 3) {{
        targetCandidates = allMunis.filter(m => m.c !== targetMuni.c);
      }}

      targetCandidates.sort(() => Math.random() - 0.5);
      const dummies = targetCandidates.slice(0, 3);

      const choices = [targetMuni, ...dummies].sort(() => Math.random() - 0.5);
      state.currentChoices = choices;

      const grid = document.getElementById('choice-buttons-grid');
      grid.innerHTML = '';

      choices.forEach(c => {{
        const btn = document.createElement('button');
        btn.className = 'choice-btn p-3 rounded-xl bg-slate-700/80 hover:bg-slate-700 text-white font-bold text-sm sm:text-base border border-slate-600/70 transition active:scale-95 text-center truncate select-none shadow';
        btn.innerHTML = `<div>${{c.n}}</div><div class="text-[11px] font-normal text-slate-400">${{c.k}}</div>`;
        btn.onclick = () => handleChoiceAnswer(c.c, btn);
        grid.appendChild(btn);
      }});
    }}

    function handleChoiceAnswer(selectedCode, clickedBtn) {{
      if (state.isAnswering) return;
      state.isAnswering = true;

      const isCorrect = selectedCode === state.currentQuestion.c;
      Store.recordAnswer(state.currentQuestion.c, isCorrect);
      updateSpokeHeaderProgress();

      const allBtns = document.querySelectorAll('.choice-btn');

      if (isCorrect) {{
        sound.playCorrect();
        clickedBtn.classList.remove('bg-slate-700/80', 'border-slate-600/70');
        clickedBtn.classList.add('bg-emerald-600', 'border-emerald-400', 'text-white');
        highlightCity(state.currentQuestion.c, 'correct');

        setTimeout(() => {{
          nextQuestion();
        }}, 900);
      }} else {{
        sound.playWrong();
        clickedBtn.classList.remove('bg-slate-700/80', 'border-slate-600/70');
        clickedBtn.classList.add('bg-rose-600', 'border-rose-400', 'text-white');
        highlightCity(state.currentQuestion.c, 'wrong');

        // 正解ボタンを緑でハイライト
        allBtns.forEach((btn, idx) => {{
          if (state.currentChoices[idx].c === state.currentQuestion.c) {{
            btn.classList.add('ring-2', 'ring-emerald-400', 'bg-emerald-700/80');
          }}
        }});

        setTimeout(() => {{
          nextQuestion();
        }}, 1800);
      }}
    }}

    /* ========================================================
       場所当てモード: ポリゴンタップ回答処理
       ======================================================== */
    function handlePolygonClick(clickedCode) {{
      if (state.currentMode === 'explore') {{
        // 探索モード: 詳細情報表示
        showExploreDetails(clickedCode);
        return;
      }}

      // 出題対象外の自治体をタップしたときの救済通知
      if (!isMuniTargetInCurrentStage(clickedCode)) {{
        const clickedMuni = MUNICIPALITIES[clickedCode];
        const name = clickedMuni ? clickedMuni.n : 'この地域';
        const lvl = clickedMuni ? clickedMuni.lvl : '';
        const type = clickedMuni ? (TYPE_LABELS[clickedMuni.t] || '市町村') : '';
        showToast(`『${{name}}』は Level ${{lvl}}（${{type}}）です（現在のLevelでは出題対象外）`);
        return;
      }}

      if (state.currentMode !== 'locate' || state.isAnswering) return;

      state.isAnswering = true;
      const isCorrect = clickedCode === state.currentQuestion.c;
      const targetMuni = state.currentQuestion;
      const clickedMuni = MUNICIPALITIES[clickedCode];

      Store.recordAnswer(targetMuni.c, isCorrect);
      updateSpokeHeaderProgress();

      const feedbackBar = document.getElementById('locate-feedback-bar');
      const feedbackContent = document.getElementById('locate-feedback-content');
      feedbackBar.classList.remove('hidden');

      if (isCorrect) {{
        sound.playCorrect();
        highlightCity(targetMuni.c, 'correct');

        feedbackContent.innerHTML = `
          <div class="flex items-center gap-2 text-emerald-400 font-bold text-sm">
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
            <span>正解！ ${{targetMuni.n}}（${{TYPE_LABELS[targetMuni.t] || ''}}）</span>
          </div>
          <button id="btn-next-fast" class="px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-xs font-bold text-white transition">次へ →</button>
        `;
        document.getElementById('btn-next-fast').onclick = () => nextQuestion();

        state.feedbackTimer = setTimeout(() => {{
          nextQuestion();
        }}, 1100);
      }} else {{
        sound.playWrong();
        highlightCity(clickedCode, 'wrong');

        // 正解の自治体をイエロー点滅でガイド
        highlightCity(targetMuni.c, 'question');

        const clickedName = clickedMuni ? clickedMuni.n : '別の自治体';

        feedbackContent.innerHTML = `
          <div class="text-xs text-rose-300 font-medium">
            <span class="font-bold text-rose-400">惜しい！</span> そこは『${{clickedName}}』です。<br>
            <span class="text-amber-300 font-semibold">黄色く光っている場所</span>が正解の『${{targetMuni.n}}』です。
          </div>
          <button id="btn-next-manual" class="px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-xs font-bold text-white transition shrink-0 active:scale-95">
            次へ →
          </button>
        `;
        document.getElementById('btn-next-manual').onclick = () => nextQuestion();
      }}
    }}

    function nextQuestion() {{
      clearTimeout(state.feedbackTimer);
      state.currentIndex++;
      loadQuestion();
    }}

    /* ========================================================
       エクスプローラーモード: 自治体詳細カード
       ======================================================== */
    function showExploreDetails(code) {{
      const muni = MUNICIPALITIES[code];
      if (!muni) return;

      // 前回のハイライト解除して今回タップしたものをイエローハイライト
      Object.keys(state.cityLayerMap).forEach(c => resetCityHighlight(c));
      highlightCity(code, 'question');

      document.getElementById('explore-empty-state').classList.add('hidden');
      document.getElementById('explore-detail-state').classList.remove('hidden');

      document.getElementById('explore-name').textContent = muni.n;
      document.getElementById('explore-kana').textContent = muni.k;
      document.getElementById('explore-type-badge').textContent = TYPE_LABELS[muni.t] || '自治体';
      document.getElementById('explore-code').textContent = muni.c;

      const rec = Store.getRecord(code);
      const statusTag = document.getElementById('explore-status-tag');
      if (rec && rec.correct > 0) {{
        statusTag.innerHTML = `<span class="text-emerald-400 font-semibold">✓ 正解履歴あり (${{rec.correct}}回)</span>`;
      }} else if (rec && rec.wrong > 0) {{
        statusTag.innerHTML = `<span class="text-rose-400 font-semibold">ミス履歴あり (${{rec.wrong}}回)</span>`;
      }} else {{
        statusTag.textContent = '未挑戦';
      }}

      // 「この自治体をテスト」ボタン
      document.getElementById('btn-explore-quiz-this').onclick = () => {{
        // 場所当てモードに切り替えてこの自治体を出題
        document.querySelector('[data-mode="locate"]').click();
        state.activeQuestionList = [muni];
        state.currentIndex = 0;
        loadQuestion();
      }};
    }}

    // アプリケーション起動
    window.addEventListener('DOMContentLoaded', () => {{
      initHub();
    }});
  </script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated index.html successfully!")
import os
print("index.html size:", os.path.getsize("index.html"), "bytes")

