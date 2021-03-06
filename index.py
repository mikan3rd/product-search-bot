import os
from io import BytesIO

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (CarouselColumn, CarouselTemplate, ImageMessage,
                            MessageEvent, TemplateSendMessage, TextMessage,
                            TextSendMessage, URITemplateAction)

import settings
from docomo import search_product

app = Flask(__name__)


line_bot_api = LineBotApi(settings.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:", body)

    # handle webhook body
    try:
        handler.handle(body, signature)

    except InvalidSignatureError as e:
        print("InvalidSignatureError:", e)
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # print("handle_message:", event)
    text = event.message.text

    messages = [
        TextSendMessage(text=text),
        TextSendMessage(text='画像を送ってみてね!'),
    ]

    reply_message(event, messages)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    # print("handle_image:", event)

    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    image = BytesIO(message_content.content)

    try:
        result = search_product(image)

        if isinstance(result, str):
            messages = [
                TextSendMessage(text=result),
                TextSendMessage(text='食品パッケージ/書籍/CD/DVD/ゲームソフト/PCソフトを検索できるよ！')
            ]

        elif isinstance(result, list):

            columns = [
                CarouselColumn(
                    thumbnail_image_url=column['thumbnail_image_url'],
                    title=column['title'],
                    text=column['text'],
                    actions=[
                        URITemplateAction(
                            label=column['actions']['label'],
                            uri=column['actions']['uri'],
                        )
                    ]
                )
                for column in result
            ]

            messages = TemplateSendMessage(
                alt_text='template',
                template=CarouselTemplate(columns=columns),
            )

        reply_message(event, messages)

    except Exception as e:
        print("error:", e)
        reply_message(event, TextSendMessage(text='エラーが発生しました'))


def reply_message(event, messages):
    line_bot_api.reply_message(
        event.reply_token,
        messages=messages,
    )


if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    app.run(
        host='0.0.0.0',
        port=port,
    )
