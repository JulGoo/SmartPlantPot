# 텔레그램 봇 인터페이스

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

# 사용자 명령어 인터페이스

## 핸들러 함수
### 다양한 명령어 및 메세지 처리

* **start()** <br>
사용자가 /start를 입력 시 실행 (초기 안내 메세지)

* **handle_message()** <br>
사용자가 텍스트 메세지를 입력 시 실행

* **unknown_command()** <br>
사용자가 알 수 없는 메세지를 입력 시 실행 (오류 처리)





