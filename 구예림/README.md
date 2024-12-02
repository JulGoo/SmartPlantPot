# 텔레그램 봇
## 텔레그램에서 봇 생성(BotFather 사용)
이름: **SmartPlantPot44_bot**

### 라이브러리 설치
```
pip install python-telegram-bot --upgrade
```

## dotenv를 활용한 Token 및 ChatID 가져오기
### 단일 사용자로 가정 후 테스트
봇의 **Token**을 사용해, **ChatID**를 확인
```
https://api.telegram.org/bot[Token]/getUpdates
```
* 이 URL을 호출하면, 봇이 받은 최근 메시지와 관련된 정보가 JSON 형식으로 반환

### .env 파일 및 .gitignore 설정

* 프로젝트 디렉토리에 `.env` 파일을 생성한 후, 봇의 **토큰 값**과 **채팅 아이디**를 추가
* **.gitignore**에 **.env**파일 추가 (**비공개 처리**)

### `python-dotenv` 설치
`.env` 파일의 값을 파이썬 코드에서 읽어오기 위해 `python-dotenv` 라이브러리를 설치
```
pip install python-dotenv
```

## def
### load_telegram()
.env에서 토큰값 / 채팅아이디 로드

### send_chat(msg, chat_id)
load_telegram()에서 가져온 chat_id로 msg 전송

### send_image(chat_id)
식물 상태 분석에서 식물의 사진과 시각화한 이미지 전송

### send_video(chat_id)
타임랩스 조회에서 영상 전송

# 사용자 명령어 인터페이스
## 인터페이스
### InlineKeyboardButton
사용자 인터페이스의 선택지를 버튼으로 생성

## def
### start()
사용자가 /start를 입력 시 실행 (초기 안내 메세지)

### button_handler()
사용자가 텍스트 메세지를 입력 시 실행

1. 도움말
2. 식물 설정
3. 식물 상태 분석 -> 시각화 결과, 식물 사진, 양호/불량
4. 타임랩스 조회 -> 영상
5. 물주기 설정
	1. 수동 물주기 
    2. 물탱크 잔여량 조회
6. 조명 설정
	1. 조명 Off 
	2. 조명 25% On 
    3. 조명 50% On 
	4. 조명 75% On 
    5. 조명 100% On 
	6. 자동 조명 관리로 전환 

### message_handler()
사용자의 임의의 메시지에 응답 (메시지 처리 핸들러)

### unknown_command()
사용자가 알 수 없는 메세지를 입력 시 실행 (오류 처리)

# 실시간 상태 보고
각 로직에서 이 함수들을 불러와 실행
## def
### time_check()
메세지가 보내진 시간을 현재 시간과 비교해 최소 1시간 이후에 보내지도록 시간 체크

### msg_water()
자동 물주기 시 알람

### msg_light()
수동 모드일 때 조도값이 부족한 경우 알람

### msg_water_tank()
물탱크 물 부족 시 알람

### msg_temp_up()
설정된 온도 임계값을 높게 벗어날 시 알람

### msg_temp_down()
설정된 온도 임계값을 낮게 벗어날 시 알람

### msg_humid_up()
설정된 습도 임계값을 높게 벗어날 시 알람

### msg_humid_down()
설정된 습도 임계값을 낮게 벗어날 시 알람





