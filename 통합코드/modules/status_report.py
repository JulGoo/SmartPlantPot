# 실시간 상태 보고
import telegram
import telegram_bot as tb

# 자동 물주기 시 알람
async def msg_water():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])
    msg = ("식물이 목이 말라요.\n"
           "물을 공급할게요!")
    await tb.send_chat(msg, chat_id)

# 자동 조명 조절 시 알람
async def msg_light():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])
    msg = ("식물이 햇빛 친구를 만나고 싶대요.\n"
           "빛을 공급할게요!")
    await tb.send_chat(msg, chat_id)

# 물탱크 물 부족 시 알람
async def msg_water_tank():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])
    msg = ("물탱크에 물이 부족해요.\n"
           "물을 채워주세요!")
    await tb.send_chat(msg, chat_id)

# 설정된 온도 임계값을 높게 벗어날 시 알람
async def msg_temp_up():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])
    msg = ("식물이 너무 덥대요.\n"
           "온도를 신경써주세요!")
    await tb.send_chat(msg, chat_id)

# 설정된 온도 임계값을 낮게 벗어날 시 알람
async def msg_temp_down():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])
    msg = ("식물이 너무 춥대요.\n"
           "온도를 신경써주세요!")
    await tb.send_chat(msg, chat_id)

# 설정된 습도 임계값을 높게 벗어날 시 알람
async def msg_humid_up():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])
    msg = ("식물이 너무 습하대요.\n"
           "습도를 신경써주세요!")
    await tb.send_chat(msg, chat_id)

# 설정된 습도 임계값을 낮게 벗어날 시 알람
async def msg_humid_down():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])
    msg = ("식물이 너무 건조하대요.\n"
           "습도를 신경써주세요!")
    await tb.send_chat(msg, chat_id)
