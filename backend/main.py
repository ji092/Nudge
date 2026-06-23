"""Python 사이드카 진입점. Phase 1: DB 초기화 + 동작 확인용 최소 실행."""
from project_manager import init_db
from shared.logger import get_logger
from window_manager import list_windows

logger = get_logger(__name__)


def main() -> None:
    init_db()
    logger.info("열린 창 %d개 감지됨", len(list_windows()))


if __name__ == "__main__":
    main()
