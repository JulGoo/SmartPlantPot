# 실시간 상태 보고
import telegram
import telegram_bot as tb


# 자동 물주기 시 알람
async def msg_water():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])
    pass



# 자동 조명 조절 시 알람
async def msg_light():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])
    pass



# 물탱크 물 부족 시 알람
async def msg_water_tank():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])

    pass


# 설정된 온도 임계값을 벗어날 시 알람
async def msg_temp():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])

    pass


# 설정된 습도 임계값을 벗어날 시 알람
async def msg_humid():
    chat_id = telegram.Bot(token=tb.load_telegram()[1])

    pass


