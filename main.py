import subprocess

# 가상 환경의 Python 경로
venv_python = r'C:\Users\yhsoo\OneDrive\바탕 화면\coding\moviePreviewAlarm\.venv\Scripts\python.exe'

# 순차적으로 실행할 Python 파일들
scripts = ['logic\cgv.py', 'logic\mega_box.py', 'logic\lotte_cinema.py']

# 각 스크립트를 실행
for script in scripts:
    try:
        # 각 스크립트를 subprocess로 실행
        result = subprocess.run([venv_python, script], check=True)
        print(f"{script} 실행 완료.")
    except subprocess.CalledProcessError as e:
        print(f"{script} 실행 중 오류 발생: {e}")