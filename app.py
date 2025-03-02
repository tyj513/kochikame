import re
import json
from linebot.models import QuickReply, QuickReplyButton, MessageAction
from linebot.models import FlexSendMessage
from linebot.models import BubbleContainer, BoxComponent, TextComponent, ImageComponent, ButtonComponent, IconComponent, SeparatorComponent

import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 讀取環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

app = Flask(__name__)
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
    "57": "歡迎女性來住微笑宿舍！",
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
    "260": "黃金傳說大決戰！節約能源大作戰",
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
    "353": "FINAL「珍重再見！兩津」大作戰",
} 


line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# JSON文件路徑（假設與app.py在同一目錄）
pic_database_path = 'merged_output_with_url.json'

# 全局變數存儲加載的數據
image_data = []

# 錯誤訊息
error_message = "找不到圖片"


def get_image_url(number):
    global image_data
    for entry in image_data:
        if number == entry['image_name']:
            return entry.get('url', None)
    return None

# 在應用啟動時加載JSON數據
def load_image_data():
    global image_data
    try:
        with open(pic_database_path, 'r', encoding='utf-8') as f:
            image_data = json.load(f)
        print(f"成功加載 {len(image_data)} 條圖片數據")
    except FileNotFoundError:
        print(f"錯誤: 找不到文件 {pic_database_path}")
        image_data = []
    except json.JSONDecodeError:
        print(f"錯誤: 無法解析 JSON 文件 {pic_database_path}")
        image_data = []

# 檢查圖片名稱格式 (例如 e00087)
def validate_image_number(message):
    pattern = r"^e\d+$"
    return re.match(pattern, message) is not None

# 從內存中查找圖片數據
def search_image_by_number(number):
    global image_data
    for entry in image_data:
        if number == entry['image_name']:
            return entry
    return None
 
# 搜尋圖片名稱與對應編號
def search_by_keyword(keyword):
    global image_data
    result = []
    for item in image_data:
        if keyword in item['text']:
            result.append(f"【編號:{item['image_name']}】{item['text']})")
    return result
                          

# 隨機抽取一個圖片
def create_quick_reply():
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="抽", text="抽")),
        QuickReplyButton(action=MessageAction(label="選單", text="menu"))
    ])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text.strip()

    # 處理「menu」指令
# 從內存中查找圖片數據並返回URL
def get_image_url(number):
    global image_data
    for entry in image_data:
        if number == entry['image_name']:
            return entry.get('url', None)
    return None
# 隨機抽取一個圖片
def random_image():
    global image_data
    if not image_data:
        return None
    return random.choice(image_data)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text.strip()

    # 處理「menu」指令
    if message.lower() == "menu":
        reply_message = "歡迎使用壽限無壽限無五卻之麵粉君之烏龍派出所動畫機器人！\n" \
                        "指令列表：\n" \
                        "- 輸入編號（例如 e00087 或 e1000）查看圖片\n" \
                        "- 輸入關鍵字搜尋圖片名稱\n" \
                        "- 輸入「抽」隨機抽取一張圖片"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        return

    # 處理「抽」指令
    if message == "抽":
        random_img = random_image()
        if random_img:
            img_url = random_img.get("url", "")
            img_name = random_img.get("image_name", "")
            
            # 直接發送URL作為文字，附帶Quick Reply按鈕
            text_message = TextSendMessage(
                text=img_url,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="抽", text="抽")),
                        QuickReplyButton(action=MessageAction(label="集數資訊", text=f"info:{img_name}"))
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, text_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無法抽取圖片，請確認數據已正確加載。"))
        return
    
    # 處理info:請求 (集數資訊)
    if message.startswith("info:"):
        image_number = message.replace("info:", "")
        img_data = search_image_by_number(image_number)
        if img_data:
            episode_number = img_data.get("episode", "未知")
            episode_title = episode_titles.get(episode_number, "未知集數")
            image_name = img_data.get("image_name", "")
            
            reply_message = f"編號: {image_name}\n集數: 第{episode_number}集\n標題: {episode_title}"
            
            # 添加 Quick Reply 按鈕到文字訊息
            text_message = TextSendMessage(
                text=reply_message,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="抽", text="抽")),
                        QuickReplyButton(action=MessageAction(label="選單", text="menu"))
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, text_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="找不到圖片資訊。"))
        return

    # 處理編號查詢 - 直接回傳URL文字
    if validate_image_number(message):
        img_url = get_image_url(message)
        if img_url:
            # 直接發送URL作為文字，附帶Quick Reply按鈕
            text_message = TextSendMessage(
                text=img_url,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="抽", text="抽")),
                        QuickReplyButton(action=MessageAction(label="集數資訊", text=f"info:{message}"))
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, text_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="找不到圖片。"))
        return

    # 處理關鍵字搜尋
    search_result = search_by_keyword(message)
    if search_result:  
        reply_message = "\n".join(search_result)
    else:
        reply_message = "找不到符合的圖片名稱。"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
if __name__ == "__main__":
    app.run()

 
