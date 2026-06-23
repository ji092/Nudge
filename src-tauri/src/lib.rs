// 샘플 IPC 명령 — React 쪽에서 invoke("greet", { name }) 로 호출 가능.
// 추후 Python 사이드카 연동 명령으로 교체될 자리.
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

// backend/venv 의 python 으로 window_manager.py 를 직접 실행해 JSON(stdout)을 그대로 돌려준다.
// 개발용 임시 방식 — 정식 사이드카 번들링은 나중 단계에서 교체.
#[tauri::command]
fn get_windows() -> Result<String, String> {
    // CARGO_MANIFEST_DIR = src-tauri/ 의 절대경로(컴파일 시점 고정).
    // tauri dev 가 실제로 어느 cwd 에서 실행되든 흔들리지 않도록 이걸 기준으로 backend/ 를 찾는다.
    let backend_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("backend");
    let python_path = backend_dir.join("venv").join("Scripts").join("python.exe");
    let script_path = backend_dir.join("window_manager.py");

    let output = std::process::Command::new(&python_path)
        .arg(&script_path)
        .current_dir(&backend_dir)
        .output()
        .map_err(|e| {
            format!(
                "python 실행 실패 (경로 확인 필요: {}): {}",
                python_path.display(),
                e
            )
        })?;

    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).into_owned());
    }

    Ok(String::from_utf8_lossy(&output.stdout).into_owned())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // 트레이/사이드카 연결 전 단계 — 플러그인은 필요한 만큼만 추가
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![greet, get_windows])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
