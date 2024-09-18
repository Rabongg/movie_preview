# 필요한 테이블 정보
CREATE TABLE movie_curtain_call_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(80) NOT NULL UNIQUE,
    period VARCHAR(60),
    theater ENUM('cgv', 'lotte', 'megabox') NOT NULL,
    created_dt DATETIME,
    is_send TINYINT(1) DEFAULT 0
);