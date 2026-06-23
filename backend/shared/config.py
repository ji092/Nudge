"""환경변수 *이름*만 참조한다. 값은 .env 에서 지영이 직접 채운다 (gitignored).
이 파일에는 절대 실제 키 값을 작성하지 않는다. (.agents/rules/Security.md 참고)
"""
import os
from dotenv import load_dotenv

load_dotenv()

KAKAO_REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
TMAP_APP_KEY = os.environ.get("TMAP_APP_KEY")
NOTION_API_TOKEN = os.environ.get("NOTION_API_TOKEN")

DB_PATH = os.environ.get("NUDGE_DB_PATH", "nudge.db")
