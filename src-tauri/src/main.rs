// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    // lib.rs 의 run() 을 호출만 함 (모바일 빌드와 진입점 공유 목적)
    nudge_lib::run()
}
