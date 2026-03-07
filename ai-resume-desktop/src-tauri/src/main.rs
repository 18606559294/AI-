// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::fs;
use std::io::Write;

#[tauri::command]
fn save_content(path: String, content: String) -> Result<(), String> {
    fs::File::create(&path)
        .and_then(|mut file| file.write_all(content.as_bytes()))
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn read_content(path: String) -> Result<String, String> {
    fs::read_to_string(&path).map_err(|e| e.to_string())
}

fn main() {
    tauri::Builder::<tauri::Wry>::new()
        .invoke_handler(tauri::generate_handler![save_content, read_content])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
