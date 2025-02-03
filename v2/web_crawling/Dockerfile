FROM python:3.11-slim

# # 시스템 패키지 업데이트 및 cron 설치 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    cron \
    wget \
    curl \
    unzip \
    ca-certificates \
    fonts-liberation \
    libvulkan1 \
    libappindicator3-1 \
    libasound2 \
    libx11-xcb1 \
    libnspr4 \
    libnss3 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Chrome 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -f

# Python 스크립트 복사
COPY . .

# Python 요구 사항 설치
RUN pip install -r requirements.txt

# 크론탭 파일 복사
COPY email-crontab /etc/cron.d/my-cron-job

# 크론탭 파일 권한 설정
RUN chmod 0644 /etc/cron.d/my-cron-job

# 크론 로그 파일 생성
RUN touch /var/log/cron.log

# 컨테이너 시작 시 cron과 python 스크립트를 실행
CMD cron && tail -f /var/log/cron.log
