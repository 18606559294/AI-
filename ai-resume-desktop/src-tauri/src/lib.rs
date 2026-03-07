// Tauri 应用程序入口点
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri::Builder::<tauri::Wry>::new()
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
