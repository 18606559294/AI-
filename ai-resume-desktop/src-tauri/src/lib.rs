// Tauri 应用程序入口点

// 使开发构建中的控制台窗口消失
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    ai_resume_desktop_lib::run()
}
