"""pywin32 기반 열린 창 목록 조회. Rust(Tauri)가 stdout 의 JSON 을 그대로 파싱한다."""
import ctypes
import json
import os

import win32con
import win32gui
import win32process
import win32api

DWMWA_CLOAKED = 14  # dwmapi.h — 작업표시줄도 이 속성으로 cloaked 창을 숨긴다.


def _is_cloaked(hwnd) -> bool:
    """DWM 이 화면에 실제로 안 그리는(cloaked) 창인지 확인 (UWP 껍데기/IME 호스트 등)."""
    cloaked = ctypes.c_int(0)
    ctypes.windll.dwmapi.DwmGetWindowAttribute(
        hwnd, DWMWA_CLOAKED, ctypes.byref(cloaked), ctypes.sizeof(cloaked)
    )
    return cloaked.value != 0


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


def _is_taskbar_window(hwnd) -> bool:
    """작업표시줄에 실제로 뜨는 창인지 속성으로 판단 (블랙리스트 없이)."""
    if _is_cloaked(hwnd):
        return False  # DWM 이 화면에 실제로 그리지 않는 창 — appwindow 여부와 무관하게 우선 제외
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if ex_style & win32con.WS_EX_APPWINDOW:
        return True  # 강제 포함
    if ex_style & win32con.WS_EX_TOOLWINDOW:
        return False
    if win32gui.GetWindow(hwnd, win32con.GW_OWNER):
        return False  # 소유자가 있는 창(대화상자 등)
    return True


def list_windows() -> list[dict]:
    """현재 떠 있는 창들을 [{title, exe, hwnd, active}] 형태로 반환."""
    active_hwnd = win32gui.GetForegroundWindow()
    windows = []

    def callback(hwnd, _):
        if (
            win32gui.IsWindowVisible(hwnd)
            and win32gui.GetWindowText(hwnd)
            and _is_taskbar_window(hwnd)
        ):
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
