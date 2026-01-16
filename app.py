# === 標準函式庫 ===
import re
import json
import random
import os
import logging
import unicodedata

# === 第三方函式庫 ===
from flask import Flask, request, abort
from dotenv import load_dotenv

# === LINE Bot SDK ===
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage,
    QuickReply, QuickReplyButton, MessageAction, FlexSendMessage,
    BubbleContainer, BoxComponent, TextComponent, ImageComponent,
    ButtonComponent, IconComponent, SeparatorComponent, SourceGroup, SourceRoom
) 
 
load_dotenv()
 
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
episode_titles = {
    "1": "兩津警員出現!?",
    "2": "從天而降的新進警員",
    "3": "空中攤販！生意興隆",
    "4": "中樂透彩的暴發戶",
    "5": "在刨冰上盡情滑雪",
    "6": "麗子發飆瘋狂追追追",
    "7": "醒來吧！冬眠警察",
    "8": "打開吧！勝鬨橋！",
    "9": "加油啊！場外相撲比賽",
    "10": "脫線‧暴走‧大爆走！拼命的交通安全講習！",
    "11": "拜訪中川的家",
    "12": "江戶人的激烈戰役",
    "13": "阿兩和麗子形影不離!?",
    "14": "迷路小象的假日",
    "15": "本田為愛奔走",
    "16": "所長家的神秘寶物",
    "17": "蟑螂大競賽",
    "18": "重現京都之旅",
    "19": "蕎麥麵屋的重振計畫！",
    "20": "兩津式的考試必勝法",
    "21": "獎金爭奪戰",
    "22": "兩津最受歡迎宣言",
    "23": "新春的戰鬥紙牌",
    "24": "日本最沒責任感的父子",
    "25": "在家關禁閉才不可怕！",
    "26": "賺收視率！",
    "27": "超級有錢人！白鳥麗次",
    "28": "阿兩大逃亡",
    "29": "男人之間的溝通橋樑－檜木澡堂",
    "30": "三月三日娃娃節",
    "31": "忍者V.S.印地安兩津",
    "32": "阿兩現在修行中",
    "33": "啊～好想有自己的房子",
    "34": "高科技小學生V.S.兩津",
    "35": "熱淚盈眶的所長",
    "36": "奪回秘密照片",
    "37": "不要命的吃到飽",
    "38": "白鳥麗次再度登場",
    "39": "熱戀中的兩津和麻里愛",
    "40": "爆笑的翻墮羅拳法",
    "41": "初戀情人是兩津！？",
    "42": "鱷魚的演藝生涯心酸史",
    "43": "呼風喚雨的棒球賽",
    "44": "兩津勘吉的閃電結婚",
    "45": "阿兩的實習生訓練記",
    "46": "阿兩的人形娃娃熱賣中",
    "47": "緊張刺激！急流中的遊船",
    "48": "阿兩男扮女裝大作戰",
    "49": "到加拿大練翻墮羅拳",
    "50": "美味的復仇食譜",
    "51": "利用幽靈賺大錢",
    "52": "激動派的超級辣媽",
    "53": "淺草初戀物語",
    "54": "超激烈的遊戲玩家－左近寺",
    "55": "造成大混亂的下流照片",
    "56": "神勇的爺爺",
    "57": "歡迎女人進來住的男生宿舍",
    "58": "所長的私生子疑案",
    "59": "出動松茸守衛隊",
    "60": "翻墮羅拳，千鈞一髮！",
    "61": "再見了，大原所長！？",
    "62": "向前衝吧！失戀的機車騎士",
    "63": "警署內的報紙大戰",
    "64": "獎金爭奪戰Part２",
    "65": "出差症候群",
    "66": "追蹤！名犬兩津",
    "67": "驚人的無厘頭新年聚會",
    "68": "對決！釣馬子",
    "69": "老爺爺和炸彈綁匪",
    "70": "本田的最後一個戀情",
    "71": "會令人上癮的美少女人形",
    "72": "燃燒吧！對露營的熱情",
    "73": "烏龍教授登場",
    "74": "絕對放心！兩津觀光",
    "75": "妖怪煙囪消失的日子",
    "76": "恐怖的置物櫃",
    "77": "欲望之真人抓娃娃機",
    "78": "激烈的社長─中川的父親",
    "79": "超烏龍的新發明",
    "80": "為種花而奮戰的阿兩",
    "81": "波爾波的同居時代",
    "82": "飛吧！警車上司",
    "83": "停不下來的攤販列車！",
    "84": "華麗的變身！月光刑警",
    "85": "未爆彈送貨到府",
    "86": "兩津死了！什麼？",
    "87": "貼緊！危險的兩人",
    "88": "擊沉！忍者老爺爺",
    "89": "恐怖的交通安全指導教官",
    "90": "鴿子咕咕刑警誕生！",
    "91": "恐怖！我的長髮怪朋友",
    "92": "大家來打棒球",
    "93": "這位就是我喜歡的人",
    "94": "從外太空掉下來的禮物",
    "95": "令人稱羨的兩人合照",
    "96": "被詛咒的梅子壺",
    "97": "中川是下町人嗎？",
    "98": "沒有牙齒就不能說的故事/阿兩要去月球了",
    "99": "我才是主角！星逃田",
    "100": "愛的貼身保鑣",
    "101": "窮途末路的最邊陲署",
    "102": "淺草的電影院樂園",
    "103": "烏龜的報恩",
    "104": "變身！所長的新車",
    "105": "獎金爭奪戰3",
    "106": "翻墮羅替身拳",
    "107": "兩津變小了！",
    "108": "淺草物語",
    "109": "哥哥的身份",
    "110": "親戚的身份",
    "111": "環遊世界48小時",
    "112": "麻里愛，愛的鐵拳！",
    "113": "逆襲！報應老頭",
    "114": "衝啊！麗子大追蹤",
    "115": "人世間嚴禁火燭",
    "116": "秘藥兩津GPX",
    "117": "本田一家--1",
    "118": "在乎，也是種戀愛",
    "119": "多采多姿的生活方式/禍從臉出",
    "120": "菜鳥刑警--兩津",
    "121": "不要叫我爸爸！",
    "122": "左近寺 全新的出發",
    "123": "遙遠的放學後......",
    "124": "離奧運開幕還早得很？",
    "125": "戀愛的沖選島",
    "126": "飛吧！航空警察隊",
    "127": "感動！寺井的初體驗",
    "128": "兩津成為漫畫家！",
    "129": "激烈的踢罐子戰爭",
    "130": "諾斯特拉兩津的大預言",
    "131": "家庭錄影帶之王",
    "132": "龜有的寧靜之夜",
    "133": "決戰！大破高爾夫球場",
    "134": "查理小林的秘密",
    "135": "荒唐深海SOS",
    "136": "工作吧!!松吉",
    "137": "在夜空中綻放的禮物",
    "138": "兩津體力有限公司",
    "139": "愛笑的惠比壽",
    "140": "撲克牌大戰",
    "141": "機械警察出動",
    "142": "史特拉第大追縱",
    "143": "宇宙人的逆襲",
    "144": "獎金爭奪戰4",
    "145": "時間啊！停止吧！/極樂啊！你在那啊！",
    "146": "遙遠的寺井家",
    "147": "靠鈣質撐過去！",
    "148": "肉體派魔術師",
    "149": "小町成為明星",
    "150": "實錄錄影帶攝影師",
    "151": "米和飯團的旅行",
    "152": "地獄般的寄宿生活",
    "153": "大哥大恐慌",
    "154": "溫泉旅行",
    "155": "不忍池的回憶",
    "156": "決戰大自然高爾夫",
    "157": "中川的平民生活苦鬥記",
    "158": "重新創造一次人生/聲音模仿家",
    "159": "人生中最倒楣的一天",
    "160": "飛越海洋的愛情",
    "161": "利用動畫卡通賺‧大‧錢！",
    "162": "友情的翅膀",
    "163": "高科技社長一家人",
    "164": "忍辱負重的工作",
    "165": "出現了！少女漫畫刑事！",
    "166": "災難的發生總是在大意時",
    "167": "終極戰警兩津",
    "168": "兩津的身體檢查",
    "169": "光輝的球場",
    "170": "下町交番日記(小地方派出所的日記)",
    "171": "劍道一直線！",
    "172": "勘吉郎的夏天",
    "173": "激烈衝突慈善義賣會",
    "174": "冬眠警官要回來了！",
    "175": "秘境！度井仲縣！",
    "176": "馬戲團交響曲",
    "177": "送報少年勘吉的故事",
    "178": "大衝突！兩津V.S.烏鴉！",
    "179": "圭一、麗子的夫妻漫才",
    "180": "阿兩開計程車",
    "181": "快跑！穩贏金太郎！",
    "182": "兩津成為藝術家",
    "183": "本田一家2--伊步的寶物",
    "184": "誤會一場",
    "185": "兩津加入選舉",
    "186": "獎金爭奪戰5",
    "187": "身體交換記",
    "188": "寺井，固執的追查",
    "189": "這裡是銀座署歌舞伎町派出所！",
    "190": "醒來吧！老實人兩津",
    "191": "大江戶搜查網",
    "192": "教你如何飼養寵物吧",
    "193": "回來了！交通安全之鬼",
    "194": "無軌電力公車的故事",
    "195": "悲慘的生日",
    "196": "聖橋的白線飄流",
    "197": "給親愛的大哥",
    "198": "人情義理的搖藍曲",
    "199": "快幫我把塗鴉擦掉啊~~~~~！",
    "200": "兩津城改造計劃",
    "201": "竊取收視率的男人",
    "202": "兩津的禁酒令",
    "203": "超級編輯",
    "204": "兩津成為有錢人",
    "205": "庶民區警察",
    "206": "超級幼稚園兒童--檸檬！",
    "207": "忍者學校開學了！",
    "208": "爸爸是孩子王！",
    "209": "憤怒的胸像~~",
    "210": "麗子，夏天的回憶......",
    "211": "在十二樓見",
    "212": "一億元爭奪戰",
    "213": "廟會太鼓",
    "214": "再見了，兩津......",
    "215": "決定！排行榜王！",
    "216": "魔法水壺",
    "217": "天才小學生的初戀(對檸檬一見鍾情)",
    "218": "超級老督察最完美的一天",
    "219": "兩津的臉",
    "220": "小心強迫推銷！",
    "221": "我是女演員--龜有兩子！",
    "222": "史上最慘之逃脫事件",
    "223": "獎金爭奪戰6",
    "224": "露餡了！小偷株式會社",
    "225": "飛向天空吧！聖誕節",
    "226": "檸檬的父親參觀日",
    "227": "飛吧！魔法飛毯",
    "228": "整人假情報的兩津鍋",
    "229": "警察便利店",
    "230": "今晚現場直播！？",
    "231": "龍蝦！螃蟹！魷魚！巨大生化生物來襲！/房客的顏色",
    "232": "熊寶寶大作戰",
    "233": "慘慘慘！悲劇重演的生日！",
    "234": "冒險家勘吉",
    "235": "打嗝止不住~~~~！",
    "236": "善良的小偷",
    "237": "兩津和檸檬的京都旅行",
    "238": "愛情大沉沒！！",
    "239": "街頭足球賽2002",
    "240": "遇見鑰匙狂",
    "241": "中川尋父三千里",
    "242": "兩津，最長的一天/星逃田警官再度登場！",
    "243": "極密任務！建造五重塔",
    "244": "本田大震撼！伊步要結婚了？！",
    "245": "高朋滿座！葛飾摔角大賽！",
    "246": "寺井跑吧！為了兒子拿到紀念章！",
    "247": "開發警用機器人004號失敗太郎登場！",
    "248": "隱形刑警出現了！",
    "249": "檸檬當姊姊了",
    "250": "一週內吃下300個西瓜的男人",
    "251": "小兩津是小妖精嗎！？",
    "252": "泳裝照大進擊",
    "253": "派出所有好溫泉！",
    "254": "火冒三丈的機器警察",
    "255": "兩津的(下町)平民之旅",
    "256": "桃太灰姑娘？/傳真我的一切！",
    "257": "利用療傷系賺大錢！",
    "258": "難纏的御所河原大爺",
    "259": "騙人的兩津和被騙的兩津",
    "260": "節約能源大作戰",
    "261": "兩津的狗兒生活",
    "262": "下町澡堂的壁畫",
    "263": "兩津撿到寶！秘密整人實況",
    "264": "獎金爭奪戰7",
    "265": "天上掉下來的......10億元！",
    "266": "飛吧！肩揹式直昇機！",
    "267": "兩津變大了！",
    "268": "大和魂保存會！？",
    "269": "兩津20面相",
    "270": "奪回彩券大作戰",
    "271": "ANGEL7女警隊V.S.狂野好漢隊！",
    "272": "檸檬的育嬰奮鬥記",
    "273": "是男人就要有野心！",
    "274": "衰運連連的三月三日女兒節！",
    "275": "兩津和兩津！？",
    "276": "這裡是雪國派出所",
    "277": "這裡是那裡？電極臭老頭！",
    "278": "大原所長迷上電動玩具",
    "279": "檸檬不喜歡吃的東西",
    "280": "3年B班，兩津老師！",
    "281": "課長！兩津勘吉！？",
    "282": "兩津和小町修成正果！？",
    "283": "命運的分歧點",
    "284": "臨別的贈禮",
    "285": "身體交換記2--兩津變麗子，麗子變兩津！？",
    "286": "飛吧！飛行船隊",
    "287": "這裡是烏龍廣播電台！",
    "288": "熱海章魚之旅",
    "289": "到底在那裡啊！龜有公園前臨時派出所",
    "290": "兩津熱愛宣言！？",
    "291": "淺草少年之阿飛正傳",
    "292": "向祖先問好",
    "293": "克服酷暑大作戰",
    "294": "檸檬化身成女忍者",
    "295": "老師是天花亂墜吹牛大王",
    "296": "我是誰！？",
    "297": "鯉魚大騷動",
    "298": "派出所的往事",
    "299": "東方快車竊盜案",
    "300": "衝吧！代跑運動會",
    "309": "只有兩人留守的派出所",
    "310": "拼啦！車站前的攤販大戰",
    "311": "獎金爭奪戰8",
    "312": "伸縮自如的橡膠兩津",
    "313": "兩津流漫畫補習班",
    "314": "我就是不想做嘛！怎樣？/正義使者，兩津？",
    "315": "奈緒子，意外的一天",
    "316": "中川家的繼承風波",
    "317": "兩津V.S.白鳥麗次打工大暴走！",
    "318": "正直者，兩津！？",
    "319": "搞笑制裁者",
    "320": "把平頭推廣到全世界吧！",
    "321": "尋回腳踏車大作戰",
    "322": "陰盛陽衰的派出所",
    "323": "歡迎來到龜有商店街！",
    "326": "超神田壽司真工夫對決",
    "327": "賞櫻真辛苦",
    "328": "兩津當電影導演！？",
    "329": "狂奔！奧之細道",
    "330": "所長，請安心養病......",
    "331": "麗子和王子的龜有假期",
    "332": "這才是男人的採草莓之旅",
    "333": "歡迎鴕鳥的來到！",
    "334": "慘烈的戰鬥將棋",
    "335": "鐵腕兩津",
    "336": "尋找日暮三千里",
    "337": "爸爸是露營行家",
    "338": "無人島高爾夫球",
    "339": "再度登場！本田一家Final",
    "342": "檸檬鬧罷工",
    "343": "變形！Before←→After",
    "344": "小頑童兩津",
    "345": "廟會的回憶",
    "346": "大家來跳舞",
    "347": "發明王兩津",
    "348": "開懷大笑......抱歉啦！",
    "349": "花之子兩津",
    "350": "加油！熊警察",
    "351": "愛戰士‧兩津勘吉",
    "352": "征服鮪魚的警察",
    "353": "FINAL「珍重再見！兩津」大作戰"
} 
 
emoji_unicode_to_chinese = {
  
    'U+1F600': '開心',  # 😀 Grinning face
    'U+1F601': '笑',  # 😁 Grinning face with smiling eyes
    'U+1F602': '笑',  # 😂 Face with tears of joy
    'U+1F603': '大笑',  # 😃 Smiling face with open mouth
    'U+1F604': '笑',  # 😄 Smiling face with open mouth and smiling eyes
    'U+1F606': '笑',  # 😆 Smiling face with open mouth and tightly-closed eyes
    'U+1F607': '天使',  # 😇 Smiling face with halo
    'U+1F608': '惡魔',  # 😈 Smiling face with horns
    'U+1F609': '眨眼',  # 😉 Winking face
    'U+1F60A': '笑',  # 😊 Smiling face with smiling eyes
    'U+1F60B': '好吃',  # 😋 Face savoring delicious food
    'U+1F60C': '放鬆',  # 😌 Relieved face
    'U+1F60E': '酷',  # 😎 Smiling face with sunglasses

    'U+1F617': '親',  # 😗 Kissing face
    'U+1F618': '親',  # 😘 Face throwing a kiss
    'U+1F62A': '打哈欠',  # 😪 Yawning face
    'U+1F62D': '哭',  # 😭 Loudly crying face
    'U+1F622': '淚',  # 😢 Crying face
    'U+1F621': '生氣',  # 😡 Pouting face
    'U+1F624': '生氣',  # 😤 Face with steam from nose
    
    'U+1F633': '臉紅',  # 😳 Flushed face
   
    'U+1F61E': '失望',  # 😞 Disappointed face

        
        
    'U+1F34E': '蘋果',
    'U+1F34A': '橘子',
    'U+1F34C': '香蕉',
    'U+1F349': '西瓜',
    'U+1F347': '葡萄',
    'U+1F353': '草莓',
    'U+1F352': '櫻桃',
    'U+1F34D': '鳳梨',
    'U+1F96D': '芒果',
    'U+1F95D': '奇異果',
    'U+1F351': '水蜜桃',
    'U+1F346': '茄子',
    'U+1F955': '胡蘿蔔',
    'U+1F33D': '玉米',
    'U+1F954': '馬鈴薯',
    'U+1F360': '地瓜',
    'U+1F952': '黃瓜',
    'U+1F96C': '青菜',
    'U+1F344': '蘑菇',
    'U+1F95C': '花生',
    'U+1F35E': '麵包',
    'U+1F956': '麵包',
    'U+1F96F': '貝果',
    'U+1F9C0': '起司',
    'U+1F355': '披薩',
    'U+1F354': '漢堡',
    'U+1F32D': '熱狗',
    'U+1F96A': '三明治',
    'U+1F32E': '墨西哥捲餅',
    'U+1F359': '飯糰',
    'U+1F363': '壽司',
    'U+1F35B': '咖哩飯',
    'U+1F35C': '拉麵',
    'U+1F95F': '餃子',
    'U+1F362': '串燒',
    'U+1F382': '蛋糕',
    'U+1F369': '甜甜圈',
    'U+1F36A': '餅乾',
    'U+1F36B': '巧克力',

    'U+1F4F1': '手機',
    'U+1F4DE': '電話',
    'U+1F4BB': '電腦',
    'U+1F5A5': '電腦',
    'U+2328': '鍵盤',
    'U+1F5B1': '滑鼠',
    'U+1F5A8': '印表機',
    'U+1F579': '遊戲',
    'U+1F4F7': '相機',
    'U+1F3A5': '攝影機',
    'U+1F4FA': '電視',
    'U+1F4FB': '收音機',
    'U+23F0': '鬧鐘',
    'U+1F4A1': '燈',
    'U+1F526': '手電筒',
    'U+1F50B': '電池',
    'U+1F50C': '插頭',
    'U+1F4E1': '天線',
    'U+1F399': '麥克風',
    'U+1F4E0': '傳真',
    'U+1F511': '鑰匙',
    'U+1F6AA': '門',
    'U+1F6CF': '床',
    'U+1F6CB': '沙發',
    'U+1F6BD': '馬桶',
    'U+1F6BF': '淋浴間',
    'U+1F6C1': '浴缸',
    'U+1FA91': '椅子',
    'U+1F5BC': '畫框',
    'U+1F4DA': '書籍',
    'U+1F4D6': '書',
    'U+2702': '剪刀',
    'U+1F58A': '原子筆',
    'U+1F58D': '蠟筆',
    'U+1F4CE': '迴紋針',
    'U+1F4CF': '尺',

    'U+1F697': '汽車',
    'U+1F695': '計程車',
    'U+1F699': '休旅車',
    'U+1F68C': '公車',
    'U+1F68E': '無軌電車',
    'U+1F3CE': '賽車',
    'U+1F693': '警車',
    'U+1F691': '救護車',
    'U+1F692': '消防車',
    'U+1F690': '廂型車',
    'U+1F69A': '貨車',
    'U+1F69B': '拖車卡車',
    'U+1F69C': '拖拉機',
    'U+1F6B2': '腳踏車',
    'U+1F6F5': '速克達',
    'U+1F3CD': '摩托車',
    'U+1F682': '火車',
    'U+1F686': '火車',
    'U+1F687': '地鐵',
    'U+1F69D': '車',
    'U+1F680': '火箭',
    'U+2708': '飛機',
    'U+1F6E9': '飛機',
    'U+1F6EB': '飛機',
    'U+1F6EC': '飛機',
    'U+26F5': '帆船',
    'U+1F6A4': '快艇',
    'U+1F6F3': '客輪',
    'U+26F4': '渡輪',
    'U+1F6A2': '輪船',
    'U+2693': '錨',
    'U+1F5FA': '地圖',
    'U+1F5FF': '石像',
    'U+1F5FD': '自由女神像',
    'U+1F5FC': '東京鐵塔',
    'U+1F3F0': '城堡',
    'U+1F3EF': '城堡',
    'U+1F309': '夜晚',
    'U+1F306': '黃昏',

    'U+26BD': '足球',
    'U+1F3C0': '籃球',
    'U+1F3C8': '橄欖球',
    'U+26BE': '棒球',
    'U+1F3BE': '網球',
    'U+1F3D0': '排球',
    'U+1F3C9': '橄欖球',
    'U+1F3B1': '撞球',
    'U+1F3D3': '桌球',
    'U+1F3F8': '羽毛球',
    'U+1F94A': '拳擊手套',
    'U+1F94B': '柔道',
    'U+26F8': '溜冰',
    'U+1F3BF': '滑雪',
    'U+1F3C4': '衝浪',
    'U+1F6B4': '腳踏車',
    'U+1F3C7': '賽馬',
    'U+1F3CA': '游泳',
    'U+1F3CB': '舉重',
    'U+1F3A4': '麥克風',
    'U+1F3A7': '耳機',
    'U+1F3BC': '五線譜',
    'U+1F3B9': '鋼琴',
    'U+1F941': '鼓',
    'U+1F3B7': '薩克斯風',
    'U+1F3BA': '小號',
    'U+1F3B8': '吉他',
    'U+1F3BB': '小提琴',
    'U+1F579': '搖桿',
    'U+1F3B2': '骰子',
    'U+1F004': '麻將',
    'U+265F': '西洋棋',
    'U+1F3C6': '獎盃',
    'U+1F947': '金牌',
    'U+1F948': '銀牌',
    'U+1F949': '銅牌',
    'U+1F3AD': '面具',

    'U+1F468': '老師',
    'U+1F469': '老師',
    'U+1F46E': '警察',
    'U+1F468': '醫生',
    'U+1F9D1 200D 2695 FE0F': '護士',
    'U+1F477': '工人',
    'U+1F473': '清潔工',
    'U+1F475': '小丑', 
    'U+1F9D1 200D 1F393': '學生'

}
app = Flask(__name__)
 
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
 
# 
MAX_IMAGE_ID = 19513  
MAX_VIDEO_ID = 110    
image_data = []
video_data = []
food_data = []

  
error_message = "找不到圖片"



def load_json_data(file_path, data_type_name="數據"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


image_data = load_json_data('merged_output_with_url.json', "圖片數據")
video_data = load_json_data('merge_video_output_with_url.json', "影片數據")
food_categorized = load_json_data('food_categorized.json', "食物分類數據")

# 食物 emoji 對應到分類 ID (6大分類)
food_emoji_to_category = {
    # 🍺 酒類飲料 (82個)
    "🍺": "beer",      # 啤酒
    "🍻": "beer",      # 乾杯
    "🍷": "beer",      # 紅酒
    "🍶": "beer",      # 清酒
    "🥂": "beer",      # 香檳
    "🍸": "beer",      # 雞尾酒
    "🍹": "beer",      # 調酒
    "🥃": "beer",      # 威士忌
    "☕": "beer",      # 咖啡
    "🍵": "beer",      # 茶
    "🥛": "beer",      # 牛奶
    "🧃": "beer",      # 果汁
    # 🍣 海鮮壽司 (76個)
    "🍣": "sushi",     # 壽司
    "🐟": "sushi",     # 魚
    "🦐": "sushi",     # 蝦
    "🦀": "sushi",     # 螃蟹
    "🐙": "sushi",     # 章魚
    "🦑": "sushi",     # 魷魚
    "🦞": "sushi",     # 龍蝦
    "🦪": "sushi",     # 牡蠣
    # 🍚 主食 (78個) - 飯麵餃子咖哩速食
    "🍚": "rice",      # 飯
    "🍱": "rice",      # 便當
    "🍙": "rice",      # 飯糰
    "🍜": "rice",      # 麵
    "🍝": "rice",      # 義大利麵
    "🍛": "rice",      # 咖哩
    "🥟": "rice",      # 餃子
    "🥡": "rice",      # 中華料理
    "🍕": "rice",      # 披薩
    "🍔": "rice",      # 漢堡
    "🌭": "rice",      # 熱狗
    "🥪": "rice",      # 三明治
    "🍟": "rice",      # 薯條
    "🌮": "rice",      # 塔可
    "🥙": "rice",      # 口袋餅
    # 🍖 肉類燒烤 (76個)
    "🍖": "meat",      # 肉
    "🍗": "meat",      # 雞腿
    "🥩": "meat",      # 牛排
    "🥓": "meat",      # 培根
    "🥓": "meat",      # 香腸
    # 🍲 鍋物蔬菜 (51個)
    "🍲": "hotpot",    # 火鍋
    "🥘": "hotpot",    # 燉鍋
    "🥗": "hotpot",    # 沙拉
    "🥬": "hotpot",    # 青菜
    "🥒": "hotpot",    # 黃瓜
    "🍄": "hotpot",    # 香菇
    "🥕": "hotpot",    # 紅蘿蔔
    "🧅": "hotpot",    # 洋蔥
    "🥚": "hotpot",    # 蛋
    "🍳": "hotpot",    # 煎蛋
    "🧄": "hotpot",    # 蒜
    # 🍰 甜點水果 (30個)
    "🍰": "dessert",   # 蛋糕
    "🎂": "dessert",   # 生日蛋糕
    "🍦": "dessert",   # 冰淇淋
    "🍩": "dessert",   # 甜甜圈
    "🍪": "dessert",   # 餅乾
    "🍫": "dessert",   # 巧克力
    "🍬": "dessert",   # 糖果
    "🍭": "dessert",   # 棒棒糖
    "🍮": "dessert",   # 布丁
    "🍉": "dessert",   # 西瓜
    "🍇": "dessert",   # 葡萄
    "🍈": "dessert",   # 哈密瓜
    "🍊": "dessert",   # 橘子
    "🍋": "dessert",   # 檸檬
    "🍌": "dessert",   # 香蕉
    "🍍": "dessert",   # 鳳梨
    "🍎": "dessert",   # 蘋果
    "🍓": "dessert",   # 草莓
    "🍑": "dessert",   # 桃子
}

def random_food_by_category(category_id):
    """根據分類 ID 隨機抽取一個食物項目"""
    global food_categorized
    if not food_categorized:
        return None
    
    category_data = food_categorized.get(category_id)
    if category_data and category_data.get("items"):
        return random.choice(category_data["items"])
    return None

def get_food_category_info(category_id):
    """取得食物分類的資訊"""
    global food_categorized
    if not food_categorized:
        return None, None
    
    category_data = food_categorized.get(category_id)
    if category_data:
        return category_data.get("emoji", "🍽️"), category_data.get("name", "未知")
    return None, None


# 新增搜尋特定集數的功能
def search_by_episode(episode_number):
    """
    搜尋特定集數的所有圖片和台詞
    
    Args:
        episode_number (str): 要搜尋的集數
        
    Returns:
        list: 包含該集數所有圖片的台詞、image_name 和 URL
    """
    results = []
    for idx, item in enumerate(image_data):
        if item.get("episode") == episode_number:
            results.append({
                "text": item.get("text", "無台詞"),
                "image_name": item.get("image_name", f"image_{idx}"),
                "url": item.get("url", ""),
                "index": idx
            })
    
    return results



# 檢查圖片名稱格式 (例如 e00087)
def validate_image_number(message):
    pattern = r"^[EeVv]\d{1,5}$"  # E, e, V, v 開頭，後面 1~5 位數字
    return re.match(pattern, message) is not None

def is_emoji(message):
    # Check if the character is an emoji
    return unicodedata.category(message) == 'So'



def normalize_image_number(message):
    pattern = r"^([EeVv])(\d{1,5})$"  
    match = re.match(pattern, message)
    if match:
        prefix = match.group(1).lower() 
        num = int(match.group(2)) 
        return f"{prefix}{num:05d}" 
    return None



# 從內存中查找圖片數據
def search_item_by_id(item_id, data_list, id_key_name):
    for entry in data_list:
        if item_id == entry.get(id_key_name):
            return entry
    return None
 
# 搜尋圖片名稱與對應編號
def search_by_keyword(keyword, strict=False):
    global image_data
    result = []
    for item in image_data:
        if strict:
            if keyword == item['text']:
                result.append(f"【{item['image_name']}】{item['text']}")
        else:
            if keyword in item['text']:
                result.append(f"【{item['image_name']}】{item['text']}")
    return result

def search_video_by_keyword(keyword, strict=False):
    global video_data
    result = []
    for item in video_data:
        if strict:
            if keyword == item['text']:
                result.append(f"【{item['video_name']}】{item['text']}")
        else:
            if keyword in item['text']:
                result.append(f"【{item['video_name']}】{item['text']}")
    return result

# 隨機抽取一個圖片
def random_image():
    global image_data
    if not image_data:
        return None
    return random.choice(image_data)

def random_video():
    global video_data
    if not video_data:
        return None
    return random.choice(video_data)

def random_food():
    global food_categorized
    if not food_categorized:
        return None
    
    # 從所有分類中收集所有食物
    all_items = []
    for category in food_categorized.values():
        if "items" in category:
            all_items.extend(category["items"])
            
    if not all_items:
        return None
        
    return random.choice(all_items)


def create_quick_reply(arg):
    if isinstance(arg, str):
        if arg == "image":
            buttons = [
                ("切換到影片模式", "/video"),
                ("抽圖", "抽"),
                ("選單", "menu")
            ]
        elif arg == "video":
            buttons = [
                ("切換到圖片模式", "/image"),
                # ("抽影片", "抽影片"),
                ("選單", "menu")
            ]
        else:
            buttons = []  
    elif isinstance(arg, list):
        buttons = arg
    else:       
        buttons = []

    items = [QuickReplyButton(action=MessageAction(label=label, text=text)) for label, text in buttons]
    return QuickReply(items=items)

 

def create_media_flex_message(media_data, media_type="image"):
    """通用建立媒體資訊 Flex Message 函數"""
    if media_type == "image":
        id_key = "image_name"
        alt_text = "圖片資訊"
        id_label = "編號"
    elif media_type == "video":
        id_key = "video_name"
        alt_text = "影片資訊"
        id_label = "編號" 
    else:
        return None 

    media_id = media_data.get(id_key, "未知")
    media_text = media_data.get("text", "")
    img_url = media_data.get("url", "")
    video_img_url = media_data.get("thumb_url", "") 
    episode_number = str(media_data.get("episode", "未知"))

    episode_title = episode_titles.get(episode_number, "未知集數")
 
    flex_content = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": img_url if media_type == "image" else (video_img_url),
            "size": "full",
            "aspectRatio": "16:9",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"{id_label}: {media_id}", "weight": "bold", "size": "md"},
                {"type": "text", "text": f"集數: 第{episode_number}集", "size": "sm", "color": "#555555"},
                {"type": "text", "text": f"標題: {episode_title}", "weight": "bold", "size": "sm", "color": "#555555"},
                {"type": "text", "text": f"說明: {media_text}", "wrap": True, "size": "sm", "color": "#555555"}
            ]
        }
    }
    
    return FlexSendMessage(alt_text=alt_text, contents=flex_content)
 
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK' 
    
def send_link_card(reply_token, title, text, url_label, url):
    flex_content = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": title, "weight": "bold", "size": "xl"},
                {"type": "text", "text": text, "margin": "md", "size": "sm", "color": "#666666", "wrap": True}
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {"type": "uri", "label": url_label, "uri": url}
                }
            ]
        }
    }
    line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text=title, contents=flex_content))
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    raw_message = event.message.text.strip()  
    user_id = event.source.user_id
     
    is_group_context = isinstance(event.source, (SourceGroup, SourceRoom))

    if is_group_context: 
        if not raw_message.startswith('/'):
            return 
        message = raw_message[1:].strip()
    else: 
        if raw_message.startswith('/'):
            message = raw_message[1:].strip()
        else:
            message = raw_message
             
    if not message:
        return
 
    if message == "qa" or message == "意見": 
        send_link_card(
            event.reply_token,
            title="意見與回報",
            text="點擊下方按鈕前往意見與回報！",
            url_label="前往填寫", 
            url="https://docs.google.com/forms/d/e/1FAIpQLSf-TFffHGb4Kvdn4NC0nfUROkg988-d9EnvJ_q5WL0q3qtPsg/viewform"  
        )
        return
        
    if message == "吃" or message == "食物":
        # 顯示6個食物分類 + 隨便抽選項
        category_quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="🎲 隨便吃", text="隨便吃")),
            QuickReplyButton(action=MessageAction(label="🍺 酒類/飲料", text="🍺")),
            QuickReplyButton(action=MessageAction(label="🍣 海鮮/壽司", text="🍣")),
            QuickReplyButton(action=MessageAction(label="🍚 主食", text="🍚")),
            QuickReplyButton(action=MessageAction(label="🍖 肉類/燒烤", text="🍖")),
            QuickReplyButton(action=MessageAction(label="🍲 鍋物/蔬菜", text="🍲")),
            QuickReplyButton(action=MessageAction(label="🍰 甜點/水果", text="🍰")),
            QuickReplyButton(action=MessageAction(label="選單", text="menu"))
        ])
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="🍽️ 想吃什麼？選一個類別吧！",
                quick_reply=category_quick_reply
            )
        )
        return
    
    if message == "隨便吃":
        # 從所有393個食物中隨機抽一個
        food_item = random_food()
        if food_item:
            image_name = food_item.get('image_name', '')
            quick_reply = create_quick_reply([
                ("再抽一個", "隨便吃"),
                ("選類別", "吃"),
                ("集數資訊", f"info:{image_name}"),
                ("選單", "menu")
            ])
            
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=food_item.get("url", ""),
                    preview_image_url=food_item.get("url", ""),
                    quick_reply=quick_reply
                )
            )
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="找不到食物資料"))
        return
 


    import re
    match = re.match(r"(ep|Ep|EP|集數)[\s:]*([0-9]+)", message)
    episode_number = match.group(2) if match else None

    if episode_number:
        # 搜尋該集數的所有台詞
        episode_results = search_by_episode(episode_number)
        
        if episode_results:
            # 組織回覆訊息
            episode_title = episode_titles.get(episode_number, "未知集數")
            reply_text = f"第{episode_number}集「{episode_title}」的台詞：\n\n"
            
            for idx, result in enumerate(episode_results, 1):
                reply_text += f"{idx}. 【{result['image_name']}】{result['text']}\n"
            
            # 如果訊息過長，分段發送
            if len(reply_text) > 5000:
                chunks = [reply_text[i:i+4000] for i in range(0, len(reply_text), 4000)]
                for chunk in chunks:
                    line_bot_api.push_message(user_id, TextSendMessage(text=chunk))
                return
            else:
                # 建立快速回覆按鈕
                quick_reply = create_quick_reply([
                    ("選單", "menu"),
                    ("抽圖", "抽")
                ])
                
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=reply_text, quick_reply=quick_reply)
                )
                return
             
           
        else:
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text=f"找不到第{episode_number}集的資料。")
            )
            return


     
    if message.lower() == "menu":
            # 注意：下面的文字內容要貼齊最左邊，不要有縮排
            reply_message = """【多人群組請以「/」開頭】 
    📸 圖片
    輸入「抽」隨機抽圖片
    輸入「e數字」取得圖片（例：e100）
    輸入「關鍵字」搜尋圖片（例：噗通、芭蕾、惠比壽）
    
    🎬 影片
    輸入「v編號」觀看影片（例：v77）
    輸入「v」查看影片列表
    輸入「v關鍵字」搜尋影片（例：v爆炸）
    
    輸入「ep數字」查看該集內容（例：ep202） 
    輸入「吃」抽選食物
    輸入「qa」意見回報"""
        quick_reply = create_quick_reply([
            ("選單", "menu"),
            ("抽圖片", "抽"),
            ("🍽️ 吃", "吃")
        ])
            
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=reply_message, quick_reply=quick_reply)
        )
        return


    elif message == "抽":
        random_img = random_image()
        if random_img:
            image_number = random_img['image_name']
            quick_reply = create_quick_reply([
                ("集數資訊", f"info:{image_number}"),
                ("再抽一次", "抽"),
                ("該集數的台詞", f"ep:{random_img['episode']}"),
                 ("🍽️ 吃", "吃"),
                ("選單", "menu")
            ])
            
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=random_img['url'],
                    preview_image_url=random_img['url'],
                    quick_reply=quick_reply
                )
            )
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無法抽取圖片，請確認數據已正確加載。"))
        return
     
    elif message == "v": 
        # 顯示所有影片列表
        video_list = []
        for item in video_data:
            video_name = item.get('video_name', '')
            normalized_id = normalize_image_number(video_name)
            text = item.get('text', '')
            episode = item.get('episode', '')
            episode_title = episode_titles.get(episode, "")
            
            video_entry = f"【{normalized_id}】{text} (第{episode}集 {episode_title})"
            video_list.append(video_entry)
            
            
        reply_message = "\n".join(video_list)
        
        if len(reply_message) > 5000:  
            chunks = [reply_message[i:i+4000] for i in range(0, len(reply_message), 4000)]
            for chunk in chunks:
                line_bot_api.push_message(event.source.user_id, TextSendMessage(text=chunk))
            return
        
        quick_reply = create_quick_reply([
            ("選單", "menu"),
            ("抽圖片", "抽")
        ])
        
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=reply_message,
                quick_reply=quick_reply
            )
        )
        return
    
    
    elif message.startswith("info:"):
        item_id_raw = message.replace("info:", "") 
        normalized_id = normalize_image_number(item_id_raw)

        if not normalized_id:
            logging.warning(f"無效的 info 格式: {item_id_raw}")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無效的編號格式。"))
            return

        logging.info(f"🔍 處理 info 請求，正規化編號: {normalized_id}")

        media_data = None
        media_type = ""
        data_list_to_search = []
        id_key_to_search = ""
        max_id_num = 0
        prefix = normalized_id[0].lower() # 'v' or 'e'
        item_num = int(normalized_id[1:]) # 數字部分


        if prefix == 'v':
            media_type = "video"
            data_list_to_search = video_data
            id_key_to_search = 'video_name'
            max_id_num = MAX_VIDEO_ID
            nav_labels = ("上一部影片", "下一部影片")
            # random_cmd = "抽影片" # 假設有抽影片指令
        elif prefix == 'e':
            media_type = "image"
            data_list_to_search = image_data
            id_key_to_search = 'image_name'
            max_id_num = MAX_IMAGE_ID
            nav_labels = ("上一張", "下一張")
            random_cmd = "抽"
        else:
            
            logging.error(f"無法識別的編號前綴: {prefix} in {normalized_id}")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="內部錯誤：無法識別的編號。"))
            return

        # 執行搜尋
        media_data = search_item_by_id(normalized_id, data_list_to_search, id_key_to_search)

        if media_data:
            logging.info(f"✅ 找到 {media_type} 資訊: {normalized_id}")

            if item_num > 1:
                prev_num_str = f"{prefix}{(item_num - 1):05d}"
            else:
                prev_num_str = normalized_id

            if item_num < max_id_num:
                next_num_str = f"{prefix}{(item_num + 1):05d}"
            else:
                next_num_str = normalized_id 



            quick_reply_buttons = [
                (nav_labels[0], prev_num_str),
                (nav_labels[1], next_num_str),
                ("該集所有台詞", "ep" + str(media_data.get("episode", "未知"))),
                ("選單", "menu")
            ]


            if prefix == 'e':
                quick_reply_buttons.insert(2, ("抽", "抽"))


 
 
            quick_reply_buttons_filtered = [(label, text) for label, text in quick_reply_buttons if text != normalized_id or label in [random_cmd, "選單"]]
            quick_reply = create_quick_reply(quick_reply_buttons_filtered)
            flex_message = create_media_flex_message(media_data, media_type)

            if flex_message:
                line_bot_api.reply_message(
                    event.reply_token,
                    [flex_message, TextSendMessage(text="請選擇操作：", quick_reply=quick_reply)]
                )
            else:
                 logging.error(f"無法為 {normalized_id} 創建 Flex Message (類型: {media_type})")
                 line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無法生成項目資訊卡片。"))

        else:
            error_msg = f"找不到指定的{media_type}資訊 ({normalized_id})。" 
            logging.warning(error_msg)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_msg))

        return # 處理完畢

    elif message.startswith("prev:") or message.startswith("next:"):
        if message.startswith("prev:"):
            current_image = message.replace("prev:", "")
            img_num = int(current_image[1:])
            target_image = f"e{img_num - 1:05d}"
        else:  # next:
            current_image = message.replace("next:", "")
            img_num = int(current_image[1:])
            target_image = f"e{img_num + 1:05d}"
            
        img_data = search_item_by_id(normalized_message, image_data, 'image_name')
        if img_data:
            quick_reply = create_quick_reply([
                ("上一張", f"prev:{target_image}"),
                ("下一張", f"next:{target_image}"),
                ("集數資訊", f"info:{target_image}"),
                ("抽", "抽")
            ])
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=img_data['url'],
                    preview_image_url=img_data['url'],
                    quick_reply=quick_reply
                )
            )
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="找不到圖片。"))
        return

    # 處理圖片編號請求
    elif validate_image_number(message):
        normalized_message = normalize_image_number(message)
        logging.info(f"🔍 處理正規化編號: {normalized_message}")

        img_data = search_item_by_id(normalized_message, image_data, 'image_name')
        vid_data = search_item_by_id(normalized_message, video_data, 'video_name')

        reply_messages = []
        quick_reply_items = []

        if img_data:
            logging.info(f"✅ 找到圖片: {normalized_message}")
            # 建立圖片 Quick Reply
            img_num = int(normalized_message[1:])
            prev_img_num_str = normalize_image_number(f'e{img_num - 1}') if img_num > 1 else "e00001" # 考慮邊界 
            next_img_num_str = normalize_image_number(f'e{img_num + 1}') if img_num < 19513 else "e19513"  

            img_quick_reply = create_quick_reply([
                ("上一張", prev_img_num_str),
                ("下一張", next_img_num_str),
                ("集數資訊", f"info:{normalized_message}"),
                ("該集所有台詞", f"ep{img_data.get('episode', '未知')}"),
                ("抽", "抽"),
                ("🍽️ 吃", "吃"),
                ("選單", "menu")
            ])
            reply_messages.append(
                ImageSendMessage(
                    original_content_url=img_data['url'],
                    preview_image_url=img_data['url'],
                    quick_reply=img_quick_reply # 將 Quick Reply 附加到圖片訊息
                )
            )

        if vid_data:
            logging.info(f"✅ 找到影片: {normalized_message}")
            # 建立影片 Quick Reply
            vid_num = int(normalized_message[1:]) # 假設影片編號規則與圖片相同
            prev_vid_num_str = normalize_image_number(f'v{vid_num - 1}') if vid_num > 1 else "v00001" # 注意前綴 'v'
            next_vid_num_str = normalize_image_number(f'v{vid_num + 1}') if vid_num < MAX_VIDEO_ID else f"v{MAX_VIDEO_ID}" # 假設有 MAX_VIDEO_ID

            vid_quick_reply = create_quick_reply([
                ("上一部影片", prev_vid_num_str),
                ("下一部影片", next_vid_num_str),
                ("集數資訊", f"info:{normalized_message}")
                # ("抽影片", "抽影片") # 假設有抽影片功能
            ]) 
            reply_messages.append(
                VideoSendMessage(
                    original_content_url=vid_data['url'],
                    preview_image_url=vid_data.get('preview_url', vid_data['url']) 
                )
            )
            reply_messages.append(
                TextSendMessage(text="請選擇影片相關操作：", quick_reply=vid_quick_reply)
            )


        if reply_messages:
            line_bot_api.reply_message(event.reply_token, reply_messages)
        else:
            logging.warning(f"❌ 找不到編號 {normalized_message} 對應的圖片或影片")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message)) # 使用全局錯誤訊息

        return  
    
    elif message.startswith("strict:"):
        keyword = message.replace("strict:", "").strip()
        search_result = search_by_keyword(keyword, strict=True)
        
        if search_result:  
            reply_message = "\n".join(search_result)
        else:
            reply_message = "找不到符合的圖片名稱。"
            
        quick_reply = create_quick_reply([
            ("選單", "menu"),
            ("抽圖", "抽")
        ])
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=reply_message,
                quick_reply=quick_reply
            )
        )
        return
        
        # === 修改開始 (替換原有的 elif len(message) <= 2: 區塊) ===
    
    # 1. 先檢查是否為食物 Emoji (獨立檢查，不限制長度)
    elif message in food_emoji_to_category:
        category_id = food_emoji_to_category[message]
        food_item = random_food_by_category(category_id)
        
        if food_item:
            emoji, category_name = get_food_category_info(category_id)
            image_name = food_item.get('image_name', '')
            
            quick_reply = create_quick_reply([
                (f"再抽{category_name}", message),
                ("抽其他食物", "吃"),
                ("集數資訊", f"info:{image_name}"),
                ("選單", "menu")
            ])
            
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=food_item.get("url", ""),
                    preview_image_url=food_item.get("url", ""),
                    quick_reply=quick_reply
                )
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"這個類別目前沒有資料喔！")
            )
        return

    # 2. 檢查是否為表情符號 (Emoji 轉中文搜尋)
    elif len(message) == 1 and is_emoji(message[0]):
        unicode_str = f'U+{ord(message[0]):X}'
        if unicode_str in emoji_unicode_to_chinese:
            chinese_meaning = emoji_unicode_to_chinese[unicode_str]
            search_result = search_by_keyword(chinese_meaning, strict=False)
            if search_result: 
                reply_message = "\n".join(search_result)
            else:
                reply_message = "找不到符合的圖片名稱。"
        else:
            reply_message = "我不認識這個表情符號！"
            
        quick_reply = create_quick_reply([("選單", "menu"), ("抽圖", "抽")])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=reply_message,
                quick_reply=quick_reply
            )
        )
        return
        

        
        # Handle single character case
        if len(message) == 1:
            search_result = search_by_keyword(message)
            if search_result:  
                reply_message = "\n".join(search_result)
            else:
                reply_message = "找不到符合的圖片名稱。"
            
            quick_reply = create_quick_reply([("選單", "menu"), ("抽圖", "抽")])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=reply_message,
                    quick_reply=quick_reply
                )
            )
            return  
   
    elif message.startswith("v"):
        print(f"🔍 搜尋影片關鍵字: {message[1:]}")  # Debugging line
        search_result = search_video_by_keyword(message[1:])
        if search_result:  
            reply_message = "\n".join(search_result)
        else:
            reply_message = "找不到符合的影片名稱。"

        quick_reply = create_quick_reply([
            ("選單", "menu")
            # ("抽影片", "抽")
        ])
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=reply_message,
                quick_reply=quick_reply
            )
        )    
    else:
        search_result = search_by_keyword(message)
        if search_result:  
            reply_message = "\n".join(search_result)
        else:
            reply_message = "找不到符合的圖片名稱。"

        
        if len(reply_message) > 5000: 
            chunks = [reply_message[i:i+4000] for i in range(0, len(reply_message), 4000)]
            for chunk in chunks:
                line_bot_api.push_message(event.source.user_id, TextSendMessage(text=chunk))
            return
        

        quick_reply = create_quick_reply([
            ("選單", "menu"),
            ("抽圖", "抽"),
            ("吃", "吃")
        ])
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=reply_message,
                quick_reply=quick_reply
            )
        )
 
if __name__ == "__main__":
    app.run(debug=True)
