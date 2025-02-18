import keyboard
from ctypes import windll, byref
from ctypes.wintypes import MSG
import win32con

class HotkeyManager:
    def __init__(self, swap_callback):
        self.swap_callback = swap_callback
        self._register_hotkeys()
    
    def _register_hotkeys(self):
        """단축키 등록"""
        try:
            if not windll.user32.RegisterHotKey(None, 1, win32con.MOD_WIN, 0xC0):
                print("Windows + ` 단축키 등록 실패. 다른 단축키를 사용합니다: 'ctrl+alt+s'")
                keyboard.add_hotkey('ctrl+alt+s', self.swap_callback)
            else:
                print("Windows + ` 단축키가 성공적으로 등록되었습니다.")
            
        except Exception as e:
            print(f"단축키 등록 중 오류 발생: {e}")
            keyboard.add_hotkey('ctrl+alt+s', self.swap_callback)
    
    def check_messages(self):
        """윈도우 메시지 처리"""
        try:
            msg = MSG()
            if windll.user32.PeekMessageA(byref(msg), None, 0, 0, win32con.PM_REMOVE):
                if msg.message == win32con.WM_HOTKEY:
                    print("핫키 감지!")
                    self.swap_callback()
                elif msg.message == win32con.WM_QUIT:
                    return False
                windll.user32.TranslateMessage(byref(msg))
                windll.user32.DispatchMessageA(byref(msg))
            return True
        except Exception as e:
            print(f"메시지 처리 중 오류 발생: {e}")
            return True 