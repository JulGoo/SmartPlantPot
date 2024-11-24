# 사용자 명령어 인터페이스
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes, CallbackQueryHandler
import status_report as sr
import telegram_bot as tb
import asyncio


# 처음 접속 시 안내 메세지
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ("안녕하세요!\n"
           "똑똑한 식물 관리 플랫폼\n"
           "\"Smart Plant Pot\" 입니다!\n"
           "\n"
           "다음 번호를 선택해주세요.")

    # GUI 버튼으로 선택지 구성
    keyboard = [
        [
            InlineKeyboardButton("1. 도움말", callback_data="help"),
            InlineKeyboardButton("2. 식물 설정", callback_data="plant_setting"),
        ],
        [
            InlineKeyboardButton("3. 식물 상태 분석", callback_data="plant_analysis"),
            InlineKeyboardButton("4. 타임랩스 조회", callback_data="get_timelapse"),
        ],
        [
            InlineKeyboardButton("5. 물주기 설정", callback_data="water_setting"),
            InlineKeyboardButton("6. 조명 설정", callback_data="light_setting"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 메시지 전송
    await update.message.reply_text(msg, reply_markup=reply_markup)


# 버튼 클릭 이벤트 핸들러
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    # 버튼 클릭 시 로딩 표시 제거
    await query.answer()

    response_msg = ""

    # 버튼의 callback_data에 따라 동작 수행
    if query.data == "help":
        response_msg = (
            "명령어 도움말\n\n"
            "1. 도움말: 사용 가능한 기능에 대한 설명\n"
            "2. 식물 설정: 관리 대상 식물 정보를 입력\n"
            "3. 식물 상태 분석: 현재 상태 분석 리포트 제공\n"
            "4. 타임랩스 조회: 촬영된 식물 타임랩스 확인\n"
            "5. 물주기 설정: 수동 물주기 및 물탱크 상태 확인\n"
            "6. 조명 설정: 조명 ON/OFF 제어"
        )
    elif query.data == "plant_setting":
        # 식물 선택 버튼 생성
        keyboard = [
            [
                InlineKeyboardButton("1. 관엽식물", callback_data="plant_1"),
                InlineKeyboardButton("2. 허브/채소류", callback_data="plant_2"),
            ],
            [
                InlineKeyboardButton("3. 다육식물/선인장", callback_data="plant_3"),
                InlineKeyboardButton("4. 화초류", callback_data="plant_4"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        response_msg = "식물을 선택해주세요."

    elif query.data.startswith("plant_"):
        # 선택한 식물에 대해 파일 생성 및 데이터 쓰기
        # 식물 유형 추출 (예: "1", "2", "3", "4")
        plant_type = query.data.split("_")[1]

        # 로컬 파일 생성 및 데이터 쓰기
        # 파일명: plant_1.txt
        file_path = f"plant_{plant_type}.txt"

        # 파일 생성 및 '1' 쓰기
        with open(file_path, "w") as file:
            file.write("1")

        response_msg = f"{plant_type} 선택되었습니다. {file_path} 파일에 '1'이 기록되었습니다."

        # 버튼을 제거하여 빈 키보드로 업데이트
        reply_markup = InlineKeyboardMarkup([])

    elif query.data == "plant_analysis":
        chat_id = query.message.chat_id
        result = await sr.send_image(chat_id)
        if result is None:
            response_msg = "사진 파일이 없습니다."
        else:
            response_msg = "식물 상태 분석 결과입니다."
    elif query.data == "get_timelapse":
        chat_id = query.message.chat_id
        result = await sr.send_video(chat_id)
        if result is None:
            response_msg = "타임랩스 영상이 없습니다."
        else:
            response_msg = "현재까지 촬영된 타임랩스 영상입니다."
    elif query.data == "water_setting":
        response_msg = (
            "물주기 설정:\n"
            "1. 수동 물주기\n"
            "2. 물탱크 잔여량 확인"
        )
    elif query.data == "light_setting":
        response_msg = (
            "조명 설정:\n"
            "1. 조명 켜기\n"
            "2. 조명 끄기"
        )

    # 클릭한 버튼에 대한 응답 메시지 전송
    if response_msg:
        # "식물 설정" 메뉴를 클릭했을 때만 식물 선택 버튼을 전송
        if query.data == "plant_setting" or query.data.startswith("plant_"):
            # 메시지와 함께 식물 선택 버튼을 갱신
            await query.edit_message_text(response_msg, reply_markup=reply_markup)
        else:
            # 그 외에는 기존 버튼을 유지하도록 설정
            await query.edit_message_text(response_msg, reply_markup=query.message.reply_markup)


# 사용자 메시지 처리 핸들러 (임의의 메시지에 응답)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 사용자가 보낸 임의의 메시지에 대해 응답
    await update.message.reply_text("안녕하세요! 똑똑한 식물 관리 플랫폼 \"SmartPlantPot\" 입니다.\n시작을 위해 \"/start\"를 입력해주세요.")


# 알 수 없는 명령어 처리 핸들러
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("잘못된 명령어입니다. 다시 입력해주세요.")


# 메인 함수
async def main():
    # 어플리케이션 생성
    application = Application.builder().token(tb.load_telegram()[0]).build()

    # 핸들러 추가
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # 애플리케이션 실행
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("텔레그램 봇 실행 중...")

    try:
        while True:
            await asyncio.sleep(1)  # 대기 상태 유지
    except KeyboardInterrupt:
        print("텔레그램 봇 종료 중...")
        await application.stop()


# 프로그램 실행
if __name__ == "__main__":
    asyncio.run(main())
