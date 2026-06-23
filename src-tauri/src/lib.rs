// 샘플 IPC 명령 — React 쪽에서 invoke("greet", { name }) 로 호출 가능.
// 추후 Python 사이드카 연동 명령으로 교체될 자리.
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // 트레이/사이드카 연결 전 단계 — 플러그인은 필요한 만큼만 추가
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
