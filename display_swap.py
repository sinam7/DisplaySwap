import sys
import time
from window_manager import WindowManager
from hotkey_manager import HotkeyManager
from virtual_desktop import VirtualDesktopManager
import win32gui
import win32con
import win32api
from threading import Thread
import pystray
from PIL import Image
import os

class DisplaySwapApp:
    def __init__(self):
        self.running = True
        self.virtual_desktop = VirtualDesktopManager()
        self.window_manager = WindowManager(self.virtual_desktop)
        self.hotkey_manager = HotkeyManager(self.window_manager.swap_windows)
        self.tray_icon = None
        
    def create_tray_icon(self):
        # 기본 아이콘으로 icon.ico 사용
        icon = Image.open("icon.ico")
        
        # 메뉴 생성
        menu = (
            pystray.MenuItem("DisplaySwap 실행 중", lambda: None, enabled=False),
            pystray.MenuItem("종료", self.quit_app)
        )
        
        self.tray_icon = pystray.Icon(
            "DisplaySwap",
            icon,
            "DisplaySwap",
            menu
        )
        
    def quit_app(self):
        self.running = False
        if self.tray_icon:
            self.tray_icon.stop()
        win32gui.PostQuitMessage(0)
        
    def run(self):
        print("\n=== 프로그램 시작 ===")
        print("디스플레이 스왑 프로그램이 실행되었습니다.")
        print("Windows + ` 키로 창 스왑을 실행할 수 있습니다.")
        
        # 트레이 아이콘 생성 및 실행
        self.create_tray_icon()
        tray_thread = Thread(target=self.tray_icon.run)
        tray_thread.daemon = True
        tray_thread.start()
        
        print("메시지 루프 시작...")
        
        # 메인 루프
        try:
            while self.running and self.hotkey_manager.check_messages():
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.quit_app()
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")
            self.quit_app()
            return 1
            
        print("\n프로그램을 종료합니다.")
        return 0

def main():
    app = DisplaySwapApp()
    return app.run()

if __name__ == "__main__":
    sys.exit(main()) 