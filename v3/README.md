# 🎬 Movie Preview Alarm - v3

이 프로젝트는 영화 시사회/무대 인사 알림을 제공하는 시스템입니다.  
v3 버전은 Python 단독으로 구현되었으며, DB 없이 JSON 파일로 발송 이력을 관리합니다.  
로컬 crontab으로 하루 2회 자동 실행됩니다.

## 🔧 필수 조건

- Python 3.11 이상
- Gmail 계정 및 앱 비밀번호

## 🛠️ 실행 방법

1. **가상 환경 만들기**

   ```bash
   python3 -m venv .venv
   ```

2. **가상 환경 활성화**

   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .\.venv\Scripts\activate
     ```

3. **필요한 패키지 설치**

   ```bash
   (.venv) pip install -r requirements.txt
   ```

4. **환경 변수 설정**

   `.env.example`을 복사하여 `.env` 파일을 만들고 값을 채웁니다.

   ```bash
   cp .env.example .env
   ```

   ```env
   # Gmail 발신 계정
   SENDER_EMAIL=your_email@gmail.com

   # Gmail 앱 비밀번호 (Gmail → 설정 → 보안 → 2단계 인증 → 앱 비밀번호)
   SENDER_KEY=xxxxxxxxxxxxxxxx

   # 수신자 이메일 (여러 명이면 쉼표로 구분)
   RECEIVER_EMAILS=a@example.com,b@example.com

   # 발송 시간 (24시간제, 기본값: 오전 9시 / 오후 3시)
   SEND_HOUR_MORNING=9
   SEND_HOUR_AFTERNOON=15
   ```

   > Gmail 앱 비밀번호 발급: [Google 계정 관리](https://myaccount.google.com) → 보안 → 2단계 인증 → 앱 비밀번호

5. **수동 실행**

   ```bash
   (.venv) python main.py
   ```

6. **crontab 등록 (자동 실행)**

   ```bash
   crontab -e
   ```

   아래 내용을 추가합니다. (경로는 실제 경로로 수정)

   ```cron
   0 9  * * * cd /path/to/v3 && /path/to/v3/.venv/bin/python main.py >> /path/to/v3/logs/cron.log 2>&1
   0 15 * * * cd /path/to/v3 && /path/to/v3/.venv/bin/python main.py >> /path/to/v3/logs/cron.log 2>&1
   ```

## 🔄 Workflow

```
1. crontab 실행 (하루 2회)
        ↓
2. 각 극장 사이트 크롤링 (Megabox, Lotte Cinema, CGV)
        ↓
3. JSON 파일(data/sent_events.json)에서 중복 이벤트 필터링
        ↓
4. 신규 이벤트가 있으면 Gmail로 이메일 발송
        ↓
5. 발송 성공한 이벤트를 JSON에 저장
```

중복 판단 기준: `극장 + 제목 + 날짜 + 행사유형` 조합의 MD5 해시

## 📁 디렉토리 구조

```
v3/
├── main.py                         # 진입점
├── config/
│   ├── settings.py                 # 환경 변수 로딩
│   └── logger.py                   # 로깅 설정
├── crawlers/
│   ├── base_crawler.py             # 추상 기반 클래스 (ABC)
│   ├── cgv.py
│   ├── megabox.py
│   └── lotte_cinema.py
├── models/
│   └── event.py                    # Event dataclass
├── services/
│   ├── email_service.py            # Gmail 발송
│   ├── storage_service.py          # JSON 읽기/쓰기/중복 체크
│   └── archive_service.py          # 월별 zip 아카이브
├── templates/
│   └── email_template.html
├── tests/                          # pytest 테스트
├── logs/                           # 자동 생성 (gitignore)
└── data/                           # 자동 생성 (gitignore)
    ├── sent_events.json
    └── archive/
```

## 🧪 테스트 실행

```bash
# 전체 테스트
pytest

# 커버리지 포함
pytest --cov=. --cov-report=term-missing --ignore=.venv
```

## ⚠️ 주의사항

- `.env`, `logs/`, `data/` 디렉토리는 gitignore에 포함되어 있으며 커밋하지 않습니다.
- Gmail 앱 비밀번호는 일반 Gmail 비밀번호와 다릅니다. 앱 비밀번호를 별도로 발급해야 합니다.
- Selenium을 사용하는 크롤러는 headless 모드로 실행됩니다.
- 발송할 신규 이벤트가 없으면 이메일을 발송하지 않습니다.
