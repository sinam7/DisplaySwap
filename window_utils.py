import win32gui
import win32con
import win32api
from ctypes import windll

class WindowUtils:
    def should_process_window(self, hwnd):
        """창을 처리해야 하는지 검증"""
        try:
            # 기본 검증
            if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                return False
                
            # 제목 검증
            title = win32gui.GetWindowText(hwnd)
            if not title or len(title.strip()) < 2:
                return False
                
            # 클래스 검증
            class_name = win32gui.GetClassName(hwnd)
            ignore_classes = [
                'Shell_TrayWnd',           # 작업 표시줄
                'Shell_SecondaryTrayWnd',  # 보조 작업 표시줄
                'Progman',                 # 바탕화면
                'WorkerW',                 # 바탕화면 관련
                'ApplicationFrameWindow',  # UWP 앱 프레임
                'Windows.UI.Core.CoreWindow',  # UWP 앱
            ]
            if class_name in ignore_classes:
                return False
                
            # 스타일 검증
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            
            # 도구 창이나 임시 창 제외
            if ex_style & win32con.WS_EX_TOOLWINDOW:
                return False
                
            # 실제 창인지 확인
            if not (style & win32con.WS_VISIBLE):
                return False
                
            return True
            
        except:
            return False
    
    def get_window_info(self, hwnd):
        """창의 현재 위치와 크기 반환"""
        rect = win32gui.GetWindowRect(hwnd)
        title = win32gui.GetWindowText(hwnd)
        return {
            "hwnd": hwnd,
            "title": title,
            "left": rect[0],
            "top": rect[1],
            "right": rect[2],
            "bottom": rect[3],
            "width": rect[2] - rect[0],
            "height": rect[3] - rect[1]
        }
    
    def get_window_state(self, hwnd):
        """창의 상태를 자세히 확인"""
        try:
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE) & 0xFFFFFFFF
            placement = win32gui.GetWindowPlacement(hwnd)
            show_cmd = placement[1] if placement else None
            
            class_name = win32gui.GetClassName(hwnd)
            if class_name in ['Shell_TrayWnd', 'Shell_SecondaryTrayWnd', 'Progman', 'WorkerW']:
                return None
            
            has_caption = bool(style & win32con.WS_CAPTION)
            has_thickframe = bool(style & win32con.WS_THICKFRAME)
            has_maximize = bool(style & win32con.WS_MAXIMIZE)
            
            is_maximized = (show_cmd == win32con.SW_SHOWMAXIMIZED) or \
                          (has_maximize and has_thickframe)
            is_snapped = (not has_caption and has_thickframe) or \
                         (has_thickframe and win32gui.GetWindowRect(hwnd)[3] >= win32api.GetSystemMetrics(1))
            
            return {
                'style': style,
                'show_cmd': show_cmd,
                'is_maximized': is_maximized,
                'is_snapped': is_snapped,
                'class_name': class_name
            }
        except Exception as e:
            print(f"창 상태 확인 실패: {e}")
            return None
    
    def move_window(self, hwnd, x_offset):
        """창을 새로운 디스플레이로 이동"""
        try:
            state = self.get_window_state(hwnd)
            if not state:
                return False
                
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            new_left = rect[0] + x_offset
            
            is_maximized = state['is_maximized']
            is_snapped = state['is_snapped']
            
            # 최대화된 창인 경우 미리 위치 보정
            if is_maximized:
                width = 1920
                height = 1080
                target_display = max(0, (new_left + 960) // 1920)  # 중앙점 기준으로 판단
                new_left = target_display * 1920
                new_top = 0
            else:
                new_top = rect[1]
            
            title = win32gui.GetWindowText(hwnd)
            print(f"\n[{title}] 이동 시작:")
            print(f"  현재 위치: left={rect[0]}, top={rect[1]}, width={width}, height={height}")
            print(f"  이동 후 예상: left={new_left}, top={new_top}, width={width}, height={height}")
            print(f"  창 상태: 최대화={is_maximized}, 스냅={is_snapped}")
            
            # 창 스타일 백업
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            
            if is_maximized or is_snapped:
                print("  최대화/스냅 상태 처리 시작")
                # 1. 창 복원 전에 스타일 수정
                new_style = style & ~win32con.WS_MAXIMIZE
                win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)
                
                # 2. 창 복원
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.PumpWaitingMessages()
                
                # 3. 이동
                print("  이동 실행")
                result = windll.user32.SetWindowPos(
                    hwnd, 
                    win32con.HWND_TOP,
                    new_left, 
                    new_top, 
                    width, 
                    height,
                    win32con.SWP_FRAMECHANGED
                )
                
                # 4. 원래 상태로 복원
                if result:
                    print("  상태 복원 시작")
                    # 스타일 복원
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
                    win32gui.PumpWaitingMessages()  # 스타일 변경이 적용되도록 대기                    
                    if is_maximized:
                        print("  최대화 복원")
                        # 새 위치에서 최대화
                        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                        win32gui.PumpWaitingMessages()  # 최대화가 적용되도록 대기
                    elif is_snapped:
                        print("  스냅 복원")
                        win32gui.SetWindowPos(
                            hwnd, 
                            win32con.HWND_TOP,
                            new_left, 
                            new_top, 
                            width, 
                            height,
                            win32con.SWP_FRAMECHANGED
                        )
                    
                    final_rect = win32gui.GetWindowRect(hwnd)
                    print(f"  최종 위치: left={final_rect[0]}, top={final_rect[1]}, width={final_rect[2]-final_rect[0]}, height={final_rect[3]-final_rect[1]}")
                
                return bool(result)
            else:
                print("  일반 창 이동 실행")
                result = windll.user32.SetWindowPos(
                    hwnd, 
                    win32con.HWND_TOP,
                    new_left, 
                    new_top, 
                    width, 
                    height,
                    win32con.SWP_NOACTIVATE
                )
                
                if result:
                    final_rect = win32gui.GetWindowRect(hwnd)
                    print(f"  최종 위치: left={final_rect[0]}, top={final_rect[1]}, width={final_rect[2]-final_rect[0]}, height={final_rect[3]-final_rect[1]}")
                
                return bool(result)
                
        except Exception as e:
            print(f"창 이동 중 예외 발생: {e}")
            return False

class DisplayUtils:
    def get_primary_width(self):
        """주 디스플레이 너비"""
        return win32api.GetSystemMetrics(0)
    
    def get_total_width(self):
        """전체 디스플레이 너비"""
        return win32api.GetSystemMetrics(78)
    
    def get_screen_left(self):
        """가상 스크린 왼쪽 좌표"""
        return win32api.GetSystemMetrics(76)
    
    def is_window_in_display1(self, win_info, margin=50):
        """창이 디스플레이 1에 있는지 확인"""
        window_center = (win_info["left"] + win_info["right"]) / 2
        return window_center <= (self.get_primary_width() + margin)
    
    def is_window_in_display2(self, win_info, margin=50):
        """창이 디스플레이 2에 있는지 확인"""
        window_center = (win_info["left"] + win_info["right"]) / 2
        return window_center >= (self.get_primary_width() - margin) 