import os
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

app = Flask(__name__)

# 設定你的 LINE Bot 憑證
LINE_CHANNEL_ACCESS_TOKEN = "2006878161"
LINE_CHANNEL_SECRET = "70b1f81090cb13cb16cd487ed5398196"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 梗圖資料庫
image_database = {
    "001": "1.jpg",
    "002": "2.jpg",
    "003": "3.jpg",
}

# 神奇海螺回應
magic_conch_responses = ["是的。", "不行。", "再試一次。", "我不知道。"]

# 產生一個隨機數字作為猜數字遊戲的答案
secret_number = random.randint(1, 10)

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    """接收 LINE Webhook 請求"""
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理使用者訊息"""
    user_text = event.message.text.strip()

    # 梗圖回應（輸入編號）
    if user_text in image_database:
        image_url = image_database[user_text]
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        )
        return

    # 隨機抽取圖片
    if user_text == "隨機來一張":
        random_image = random.choice(list(image_database.values()))
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url=random_image, preview_image_url=random_image)
        )
        return

    # 神奇海螺占卜
    if user_text == "神奇海螺":
        reply_text = random.choice(magic_conch_responses)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_text)
        )
        return

    # 猜數字遊戲
    if user_text.isdigit():
        guess = int(user_text)
        if guess == secret_number:
            reply_text = f"🎉 恭喜你答對了！數字是 {secret_number}！"
        elif guess < secret_number:
            reply_text = "太小了，再試一次！"
        else:
            reply_text = "太大了，再試一次！"

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_text)
        )
        return

    # 預設回應
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="請輸入編號來獲取梗圖，或輸入「隨機來一張」試試！")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
