"""pywin32 기반 열린 창 목록 조회. Frontend 의 🟢(활성)/⚫(비활성) 표시에 쓰일 원본 데이터만 제공."""
import win32gui

from shared.logger import get_logger

logger = get_logger(__name__)


def list_windows() -> list[dict]:
    """현재 떠 있는 창들을 [{title, is_active}] 형태로 반환."""
    active_hwnd = win32gui.GetForegroundWindow()
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            windows.append(
                {
                    "title": win32gui.GetWindowText(hwnd),
                    "is_active": hwnd == active_hwnd,
                }
            )

    win32gui.EnumWindows(callback, None)
    return windows


if __name__ == "__main__":
    for w in list_windows():
        mark = "🟢" if w["is_active"] else "⚫"
        print(f"{mark} {w['title']}")
