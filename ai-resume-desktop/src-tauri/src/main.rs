// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::new()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .setup(|app| {
            #[cfg(desktop)]
            {
                let handle = app.handle();
                // 添加系统托盘
                use tauri::{SystemTray, SystemTrayEvent, SystemTraySubmenu};
                SystemTray::new()
                    .with_id("main-tray")
                    .with_icon(
                        app.default_window_icon(),
                        Some::<&str>"".into())
                    )
                    .with_menu(
                        &app,
                        SystemTraySubmenu::new()
                            .with_items(&[
                            SystemTraySubmenu::new(
                                &app,
                                "显示",
                                true,
                                Some("show").into(),
                                None,
                                None
                            ),
                            SystemTraySubmenu::new(
                                &app,
                                "隐藏",
                                true,
                                Some("hide").into(),
                                None,
                                None
                            ),
                            SystemTraySubmenu::new(
                                &app,
                                "退出",
                                true,
                                Some("quit").into(),
                                None,
                                None
                            ),
                        ])
                    )?
                    .on_menu_event(move |app, event| match event.id.as_ref() {
                        "show" => {
                            let window = app.get_window("main").unwrap();
                            window.show().unwrap();
                            window.set_focus().unwrap();
                        },
                        "hide" => {
                            let window = app.get_window("main").unwrap();
                            window.hide().unwrap();
                        },
                        "quit" => {
                            app.exit(0);
                        },
                        _ => {}
                    })?;
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
