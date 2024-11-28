# 실시간 상태 보고
import telegram_bot as tb
import datetime

time_water = None
time_water_tank = None
time_light = None
time_temp_up = None
time_temp_down = None
time_humid_up = None
time_humid_down = None


# 메세지 보낸 시간 체크
def time_check(get_time):
    current_time = datetime.datetime.now()
    if get_time is None:  # 초기값 처리
        return datetime.timedelta.max
    time_diff = current_time - get_time
    return time_diff


# 자동 물주기 시 알람
async def msg_water():
    global time_water

    chat_id = tb.load_telegram()[1]
    msg = ("식물이 목이 말라요.\n"
           "물을 공급할게요!")

    if time_check(time_water) >= datetime.timedelta(hours=1):
        await tb.send_chat(msg, chat_id)

    # 전역 변수 값 변경
    time_water = datetime.datetime.now()  # 메시지 보낼 때의 시간을 설정


# 물탱크 물 부족 시 알람
async def msg_water_tank():
    global time_water_tank

    chat_id = tb.load_telegram()[1]
    msg = ("물탱크에 물이 부족해요.\n"
           "물을 채워주세요!")

    if time_check(time_water_tank) >= datetime.timedelta(hours=1):
        await tb.send_chat(msg, chat_id)

    # 전역 변수 값 변경
    time_water_tank = datetime.datetime.now()  # 메시지 보낼 때의 시간을 설정


# 자동 조명 조절 시 알람
async def msg_light():
    global time_light

    chat_id = tb.load_telegram()[1]
    msg = ("식물이 햇빛 친구를 만나고 싶대요.\n"
           "빛을 공급할게요!")

    if time_check(time_light) >= datetime.timedelta(hours=1):
        await tb.send_chat(msg, chat_id)

    # 전역 변수 값 변경
    time_light = datetime.datetime.now()  # 메시지 보낼 때의 시간을 설정


# 설정된 온도 임계값을 높게 벗어날 시 알람
async def msg_temp_up():
    global time_temp_up

    chat_id = tb.load_telegram()[1]
    msg = ("식물이 너무 덥대요.\n"
           "온도를 신경써주세요!")

    if time_check(time_temp_up) >= datetime.timedelta(hours=1):
        await tb.send_chat(msg, chat_id)

    # 전역 변수 값 변경
    time_temp_up = datetime.datetime.now()  # 메시지 보낼 때의 시간을 설정


# 설정된 온도 임계값을 낮게 벗어날 시 알람
async def msg_temp_down():
    global time_temp_down

    chat_id = tb.load_telegram()[1]
    msg = ("식물이 너무 춥대요.\n"
           "온도를 신경써주세요!")

    if time_check(time_temp_down) >= datetime.timedelta(hours=1):
        await tb.send_chat(msg, chat_id)

    # 전역 변수 값 변경
    time_temp_down = datetime.datetime.now()  # 메시지 보낼 때의 시간을 설정


# 설정된 습도 임계값을 높게 벗어날 시 알람
async def msg_humid_up():
    global time_humid_up

    chat_id = tb.load_telegram()[1]
    msg = ("식물이 너무 습하대요.\n"
           "습도를 신경써주세요!")

    if time_check(time_humid_up) >= datetime.timedelta(hours=1):
        await tb.send_chat(msg, chat_id)

    # 전역 변수 값 변경
    time_humid_up = datetime.datetime.now()  # 메시지 보낼 때의 시간을 설정


# 설정된 습도 임계값을 낮게 벗어날 시 알람
async def msg_humid_down():
    global time_humid_down

    chat_id = tb.load_telegram()[1]
    msg = ("식물이 너무 건조하대요.\n"
           "습도를 신경써주세요!")

    if time_check(time_humid_down) >= datetime.timedelta(hours=1):
        await tb.send_chat(msg, chat_id)

    # 전역 변수 값 변경
    time_humid_down = datetime.datetime.now()  # 메시지 보낼 때의 시간을 설정
