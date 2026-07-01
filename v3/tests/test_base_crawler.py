from crawlers.base_crawler import BaseCrawler


def test_extract_event_type_returns_무대인사_when_title_contains_무대인사():
    result = BaseCrawler._extract_event_type("[무대인사] 어벤져스")
    assert result == "무대인사"


def test_extract_event_type_returns_시사회_when_title_contains_시사():
    result = BaseCrawler._extract_event_type("시사회 초대 이벤트")
    assert result == "시사회"


def test_extract_event_type_returns_커튼콜_when_title_contains_커튼콜():
    result = BaseCrawler._extract_event_type("커튼콜 행사 안내")
    assert result == "커튼콜"


def test_extract_event_type_returns_기타_when_no_keyword_matches():
    result = BaseCrawler._extract_event_type("일반 상영 안내")
    assert result == "기타"


def test_extract_event_type_returns_기타_for_empty_string():
    result = BaseCrawler._extract_event_type("")
    assert result == "기타"
