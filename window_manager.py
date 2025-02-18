import win32gui
import win32con
import win32api
from ctypes import windll
from window_utils import WindowUtils, DisplayUtils

class WindowManager:
    def __init__(self, virtual_desktop_manager):
        self.virtual_desktop = virtual_desktop_manager
        self.utils = WindowUtils()
        self.display = DisplayUtils()
    
    def get_current_desktop_windows(self):
        """현재 가상 데스크탑의 창들만 가져오기"""
        current_windows = []
        
        def enum_window_proc(hwnd, results):
            if not self.utils.should_process_window(hwnd):
                return True
                
            if self.virtual_desktop.is_window_on_current_desktop(hwnd):
                title = win32gui.GetWindowText(hwnd)
                print(f"창 '{title}' - 현재 가상 데스크탑")
                results.append(hwnd)
            
            return True
            
        try:
            print("\n=== 가상 데스크탑 창 검색 시작 ===")
            windows = []
            win32gui.EnumWindows(enum_window_proc, windows)
            print(f"=== 검색 완료: {len(windows)}개 창 발견 ===\n")
            return windows
        except Exception as e:
            print(f"창 검색 실패: {str(e)}")
            return []
    
    def move_window_to_another_display(self, hwnd, x_offset):
        """창을 다른 디스플레이로 이동"""
        return self.utils.move_window(hwnd, x_offset)
    
    def swap_windows(self):
        """디스플레이 간 창 스왑"""
        windows = self.get_current_desktop_windows()
        primary_width = self.display.get_primary_width()
        
        display1_windows = []
        display2_windows = []
        
        # 창 분류
        for hwnd in windows:
            win_info = self.utils.get_window_info(hwnd)
            if self.display.is_window_in_display1(win_info):
                display1_windows.append(hwnd)
            elif self.display.is_window_in_display2(win_info):
                display2_windows.append(hwnd)
        
        # 창 이동
        for hwnd in display1_windows:
            self.move_window_to_another_display(hwnd, primary_width)
        
        for hwnd in display2_windows:
            self.move_window_to_another_display(hwnd, -primary_width) 