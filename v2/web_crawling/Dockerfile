FROM ubuntu:latest

# 패키지 업데이트 및 필요한 패키지 설치 (한 번에 실행)
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    gnupg \
    ca-certificates \
    curl \
    unzip \
    cron \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    xfonts-base \
    xfonts-75dpi \
    fonts-liberation \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip \
    && rm -f /usr/bin/python3 && ln -s /usr/bin/python3.11 /usr/bin/python3 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 \
    && apt-get clean

# Chrome 설치
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -fy \
    && rm -f google-chrome-stable_current_amd64.deb

# 시간 동기화
ENV TZ Asia/Seoul

# 작업 디렉토리 설정
WORKDIR /app

# Python 스크립트 복사
COPY . .

# Python 요구 사항 설치
RUN pip install -r requirements.txt

# Crontab 설정 추가
RUN cp cron.sh /etc/cron.d/mycron \
    && chmod 0644 /etc/cron.d/mycron \
    && crontab /etc/cron.d/mycron \
    && touch /var/log/cron.log

# 컨테이너 시작 시 cron 실행
CMD ["cron", "-f"]
