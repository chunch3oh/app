from django.shortcuts import render

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == "hi":
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='功能表',
                                text='請選擇需要的服務',
                                actions=[
                                    MessageTemplateAction(
                                        label='霜淇淋',
                                        text='霜淇淋'
                                    ),
                                    MessageTemplateAction(
                                        label='相片沖印',
                                        text='相片沖印'
                                    ),
                                    MessageTemplateAction(
                                        label='廁所',
                                        text='廁所'
                                    )
                                ]
                            )
                        )
                    )
                elif event.message.text == "霜淇淋" or event.message.text == "相片沖印" or event.message.text == "廁所":
                    #servive = Crawler(event.message.text)
 
                    line_bot_api.reply_message(  # 回應前五間最高人氣且營業中的餐廳訊息文字
                        event.reply_token,
                        TextSendMessage(text="還沒寫好這個功能 ㄎ")
                        #TextSendMessage(text=servive.scrape()) 寫好後換這個
                    )
                else:
                    line_bot_api.reply_message(  # 回應前五間最高人氣且營業中的餐廳訊息文字
                        event.reply_token,
                        TextSendMessage(text="試試看傳「hi」")
                    )
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()