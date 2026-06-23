"""pywin32 기반 열린 창 목록 조회. Rust(Tauri)가 stdout 의 JSON 을 그대로 파싱한다."""
import json
import os

import win32con
import win32gui
import win32process
import win32api


def _exe_name(pid: int) -> str:
    """PID 로 프로세스 핸들을 열어 실행파일명만 추출. 권한 부족 시 빈 문자열."""
    try:
        handle = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid
        )
        path = win32process.GetModuleFileNameEx(handle, 0)
        return os.path.basename(path)
    except Exception:
        return ""


def list_windows() -> list[dict]:
    """현재 떠 있는 창들을 [{title, exe, hwnd, active}] 형태로 반환."""
    active_hwnd = win32gui.GetForegroundWindow()
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            windows.append(
                {
                    "title": win32gui.GetWindowText(hwnd),
                    "exe": _exe_name(pid),
                    "hwnd": hwnd,
                    "active": hwnd == active_hwnd,
                }
            )

    win32gui.EnumWindows(callback, None)
    return windows


if __name__ == "__main__":
    # ensure_ascii=True(기본값) — Windows 콘솔 코드페이지(cp949 등)와 무관하게
    # 항상 순수 ASCII 로만 출력되어 Rust 쪽 JSON 파싱이 깨지지 않는다.
    print(json.dumps(list_windows()))
