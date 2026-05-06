# Movie Preview Alarm v3 - 아키텍처 설계

## 1. 전체 흐름

```
[로컬 cron / Task Scheduler]
        │
        ▼
   main.py 실행
        │
        ├─── [ArchiveService] ─────────────────────────────┐
        │      전월 데이터 zip 아카이브                     │
        │      2개월 지난 zip 파일 삭제                     │
        │                                                   │
        ├─── [Crawlers] ──────────────────────────────────┐│
        │      CGV / Megabox / LotteCinema               ││
        │      각각 독립 실행, 실패해도 나머지 계속        ││
        │                                                  ││
        ▼                                                  ││
  [StorageService]                                         ││
  sent_events.json 로드                                    ││
  새 이벤트만 필터링 (중복 제거)                           ││
        │                                                  ││
        ▼                                                  ││
  [EmailService]                                           ││
  새 이벤트가 있으면 HTML 이메일 발송                      ││
  복수 수신자에게 동시 발송                                ││
        │                                                  ││
        ▼                                                  ││
  [StorageService]                                         ││
  발송된 이벤트 ID를 JSON에 저장                           ││
        │                                                  ││
        ▼                                                  ││
  [Logger] 전체 실행 결과 기록 ──────────────────────────┘┘
```

---

## 2. 프로젝트 디렉토리 구조

```
v3/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .env                            # 환경 변수 (gitignore)
├── .env.example                    # 환경 변수 예시
├── main.py                         # 진입점
│
├── config/
│   └── settings.py                 # .env 로딩 및 설정값 관리
│
├── crawlers/
│   ├── base_crawler.py             # 추상 기반 클래스
│   ├── cgv.py
│   ├── megabox.py
│   └── lotte_cinema.py
│
├── models/
│   └── event.py                    # 이벤트 데이터 모델 (dataclass)
│
├── services/
│   ├── email_service.py            # Gmail SMTP 발송
│   ├── storage_service.py          # JSON 읽기/쓰기, 중복 체크
│   └── archive_service.py          # 월별 zip 아카이브 및 오래된 파일 삭제
│
├── templates/
│   └── email_template.html         # 이메일 HTML 템플릿
│
├── tests/
│   ├── conftest.py                 # 공통 fixture
│   ├── fixtures/
│   │   ├── cgv_sample.html         # CGV mock HTML
│   │   ├── megabox_sample.html     # Megabox mock HTML
│   │   └── lotte_sample.html       # Lotte mock HTML
│   ├── test_event.py
│   ├── test_storage_service.py
│   ├── test_archive_service.py
│   ├── test_email_service.py
│   ├── test_cgv.py
│   ├── test_megabox.py
│   ├── test_lotte_cinema.py
│   └── test_main.py               # 통합 테스트
│
├── logs/
│   └── app.log                    # 자동 생성 (gitignore)
│
└── data/
    ├── sent_events.json            # 발송 이력 (자동 생성, gitignore)
    └── archive/
        ├── 2025-04.zip
        └── 2025-05.zip
```

---

## 3. 핵심 모듈 설계

### 3-1. Event 모델 (`models/event.py`)

```python
@dataclass
class Event:
    theater: str          # CGV / Megabox / LotteCinema
    event_type: str       # 무대인사 / 시사회
    title: str            # 영화 제목
    date: str             # 행사 날짜 (YYYY-MM-DD)
    time: str             # 행사 시간 (HH:MM), 없으면 빈 문자열
    location: str         # 극장 지점명
    actors: list[str]     # 배우/감독 목록, 없으면 빈 리스트
    booking_url: str      # 예매 링크, 없으면 빈 문자열

    @property
    def event_id(self) -> str:
        # 중복 판단용 고유 ID
        key = f"{self.theater}_{self.title}_{self.date}_{self.event_type}"
        return hashlib.md5(key.encode()).hexdigest()
```

### 3-2. BaseCrawler (`crawlers/base_crawler.py`)

```python
class BaseCrawler(ABC):
    @abstractmethod
    def crawl(self) -> list[Event]:
        """크롤링 결과를 Event 리스트로 반환. 실패 시 빈 리스트 반환."""
        pass
```

### 3-3. StorageService (`services/storage_service.py`)

- `load()` → JSON 파일에서 발송된 event_id 집합 로드
- `filter_new(events)` → 발송 이력에 없는 이벤트만 반환
- `save(events)` → 발송된 이벤트를 JSON에 추가 저장

**sent_events.json 구조:**
```json
{
  "sent": [
    {
      "id": "a1b2c3d4...",
      "title": "어벤져스",
      "theater": "CGV",
      "date": "2025-06-01",
      "event_type": "무대인사",
      "sent_at": "2025-06-01T09:00:00"
    }
  ]
}
```

### 3-4. ArchiveService (`services/archive_service.py`)

- `run()` → 아카이브 정리 + 오래된 파일 삭제를 한 번에 실행
- `archive_previous_month()` → 전월 데이터를 `data/archive/YYYY-MM.zip`으로 압축
- `cleanup_old_archives()` → 2개월 이상 지난 zip 파일 삭제

**아카이브 디렉토리 구조:**
```
data/
├── sent_events.json          # 현재 월 + 이전 데이터 (아카이브 전)
└── archive/
    ├── 2025-03.zip           # 삭제 대상 (2개월 초과)
    ├── 2025-04.zip           # 보관
    └── 2025-05.zip           # 보관
```

### 3-5. EmailService (`services/email_service.py`)

- Gmail SMTP SSL (포트 465)
- 수신자 목록을 `,`로 분리하여 복수 발송
- HTML 템플릿 렌더링 후 발송

### 3-6. 로깅 설정 (`config/settings.py` 또는 별도 `config/logger.py`)

```python
# RotatingFileHandler: 최대 5MB, 백업 3개
# 콘솔 + 파일 동시 출력
# 포맷: [YYYY-MM-DD HH:MM:SS] LEVEL - message
```

---

## 4. TDD 개발 순서

각 단계에서 테스트 먼저 작성 → 구현 → 리팩토링 순서로 진행.

```
1단계: models/event.py
  └─ test_event.py: event_id 해시 일관성, 동일 입력 동일 해시

2단계: services/storage_service.py
  └─ test_storage_service.py: 저장/로드/필터, JSON 없을 때 자동 생성

3단계: services/archive_service.py
  └─ test_archive_service.py: 월별 zip 생성, 2개월 초과 파일 삭제

4단계: services/email_service.py
  └─ test_email_service.py: smtplib mock, 복수 수신자, HTML 포함 여부

5단계: crawlers/ (각 극장별)
  └─ test_cgv.py / test_megabox.py / test_lotte_cinema.py
     fixture HTML 파싱 → Event 리스트 반환 검증

6단계: main.py 통합 테스트
  └─ test_main.py: 전체 흐름 mock 통합 검증
```

---

## 5. 테스트 구조

### Fixture 파일 활용 (크롤러 mock)

```python
# tests/conftest.py
@pytest.fixture
def cgv_html():
    with open("tests/fixtures/cgv_sample.html", encoding="utf-8") as f:
        return f.read()

# tests/test_cgv.py
def test_cgv_parse(cgv_html, mocker):
    mocker.patch("crawlers.cgv.fetch_page", return_value=cgv_html)
    crawler = CGVCrawler()
    events = crawler.crawl()
    assert len(events) > 0
    assert events[0].theater == "CGV"
```

### 이메일 mock

```python
# tests/test_email_service.py
def test_send_email(mocker):
    mock_smtp = mocker.patch("smtplib.SMTP_SSL")
    service = EmailService(settings)
    service.send(events)
    mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_once()
```

---

## 6. 실행 방식 (로컬 스케줄)

### macOS (crontab)

```bash
# crontab -e
0 9  * * * /path/to/.venv/bin/python /path/to/v3/main.py
0 15 * * * /path/to/.venv/bin/python /path/to/v3/main.py
```

### Windows (Task Scheduler)
작업 스케줄러에서 매일 09:00, 15:00에 `python main.py` 실행 등록.

---

## 7. 오류 처리 전략

| 상황 | 처리 방법 |
|------|----------|
| 특정 극장 크롤링 실패 | ERROR 로그 기록, 해당 극장 skip, 나머지 정상 처리 |
| 새 이벤트 없음 | INFO 로그 기록, 이메일 발송 안 함 |
| 이메일 발송 실패 | ERROR 로그 기록, JSON 저장 안 함 (다음 실행 시 재시도) |
| JSON 파일 없음 | 자동 생성 |
| 아카이브 실패 | ERROR 로그 기록, 메인 플로우는 계속 진행 |

---

## 8. v2 대비 변경 사항

| 항목 | v2 | v3 |
|------|----|----|
| 언어 | Python + Spring Boot | Python 단독 |
| 저장소 | MySQL + Redis | JSON 파일 |
| 인프라 | Docker | 없음 |
| 스케줄 | Docker cron | 로컬 crontab |
| 로깅 | Loki + Promtail | RotatingFileHandler |
| 테스트 | 없음 | pytest + TDD |
| 복잡도 | 높음 | 낮음 |
