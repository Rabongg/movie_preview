# Movie Preview Alarm v3 - CLAUDE.md

## 프로젝트 개요

CGV, Megabox, Lotte Cinema의 무대인사/시사회 정보를 크롤링하여 하루 2회 이메일로 알림 발송하는 Python 서비스.
DB 없이 JSON 파일로 발송 이력을 관리하며, 로컬 cron으로 실행한다.

## 기술 스택

- **언어**: Python 3.11+
- **크롤링**: Selenium + BeautifulSoup (사이트에 따라 선택)
- **이메일**: Gmail SMTP SSL (smtplib)
- **스케줄**: 로컬 crontab (macOS) / Task Scheduler (Windows)
- **저장**: JSON 파일 (`data/sent_events.json`)
- **아카이브**: 월별 zip 압축 (`data/archive/`), 2개월 초과 자동 삭제
- **로깅**: Python logging + RotatingFileHandler (`logs/app.log`)
- **설정**: python-dotenv (`.env` 파일)
- **테스트**: pytest, pytest-mock, pytest-cov

## 디렉토리 구조

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
├── tests/
│   ├── conftest.py
│   ├── fixtures/                   # 크롤러 mock HTML 파일
│   │   ├── cgv_sample.html
│   │   ├── megabox_sample.html
│   │   └── lotte_sample.html
│   ├── test_event.py
│   ├── test_storage_service.py
│   ├── test_archive_service.py
│   ├── test_email_service.py
│   ├── test_cgv.py
│   ├── test_megabox.py
│   ├── test_lotte_cinema.py
│   └── test_main.py
├── logs/                           # 자동 생성 (gitignore)
└── data/                           # 자동 생성 (gitignore)
    ├── sent_events.json
    └── archive/
```

## 핵심 설계 원칙

1. **크롤러 독립성**: 각 극장 크롤러는 실패해도 나머지에 영향 없음. `try/except`로 감싸고 빈 리스트 반환.
2. **중복 방지**: `극장+제목+날짜+행사유형` MD5 해시를 event_id로 사용. 발송 성공 후에만 JSON 저장.
3. **새 이벤트 없으면 발송 안 함**: 빈 이메일 방지.
4. **새 극장 추가 방법**: `BaseCrawler`를 상속하여 `crawl() -> list[Event]`만 구현하면 됨.

## TDD 사이클 (필수)

테스트 전부 작성 후 구현하는 방식은 TDD가 아님. 반드시 아래 사이클을 지킨다.

```
1. 테스트 하나 작성
2. pytest 실행 → RED (실패) 확인
3. 최소한의 코드로 구현
4. pytest 실행 → GREEN (통과) 확인
5. 다음 테스트로 이동
```

## 커밋 컨벤션

기능 하나 완성 시 바로 커밋. 형식: `[v3] [action] description` (1줄)

action: `add` | `test` | `update` | `fix` | `refactor`

```bash
# 예시
git commit -m "[v3] [test] add test_event.py for Event model"
git commit -m "[v3] [add] Event dataclass with event_id property"
git commit -m "[v3] [add] StorageService with JSON read/write/filter"
git commit -m "[v3] [fix] CGV date parsing for same-day events"
```

## 테스트 실행

```bash
# 전체 테스트
pytest

# 커버리지 포함
pytest --cov=. --cov-report=term-missing --ignore=.venv

# 특정 모듈만
pytest tests/test_storage_service.py
```

## 환경 변수 (`.env`)

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_KEY=your_gmail_app_password
RECEIVER_EMAILS=a@example.com,b@example.com
SEND_HOUR_MORNING=9
SEND_HOUR_AFTERNOON=15
```

## 주의사항

- `.env`, `logs/`, `data/`는 절대 커밋하지 않음 (`.gitignore`에 포함)
- Gmail 앱 비밀번호 사용 (Gmail 설정 → 2단계 인증 → 앱 비밀번호)
- Selenium 사용 시 headless 모드로 실행
- 크롤러 테스트는 실제 네트워크 요청 없이 `tests/fixtures/` HTML로만 테스트
- 아카이브 실패는 메인 플로우를 막지 않음

## 문서

- [요구사항 정의서](docs/requirements.md)
- [아키텍처 설계](docs/architecture.md)
