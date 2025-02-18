from ctypes import WINFUNCTYPE, c_int, c_void_p, POINTER, Structure, windll, byref
from comtypes import GUID

class IVirtualDesktopManagerVtbl(Structure):
    _fields_ = [
        ('QueryInterface', c_void_p),
        ('AddRef', c_void_p),
        ('Release', c_void_p),
        ('IsWindowOnCurrentVirtualDesktop', WINFUNCTYPE(c_int, c_void_p, c_void_p, POINTER(c_int))),
        ('GetWindowDesktopId', c_void_p),
        ('MoveWindowToDesktop', c_void_p)
    ]

class IVirtualDesktopManager(Structure):
    _fields_ = [('lpVtbl', POINTER(IVirtualDesktopManagerVtbl))]

class VirtualDesktopManager:
    def __init__(self):
        self.manager = None
        self._initialize_manager()
    
    def _initialize_manager(self):
        try:
            CLSID_VirtualDesktopManager = GUID("{AA509086-5CA9-4C25-8F95-589D3C07B48A}")
            IID_IVirtualDesktopManager = GUID("{A5CD92FF-29BE-454C-8D04-D82879FB3F1B}")
            
            manager = POINTER(IVirtualDesktopManager)()
            hr = windll.ole32.CoCreateInstance(
                byref(CLSID_VirtualDesktopManager),
                None,
                1,
                byref(IID_IVirtualDesktopManager),
                byref(manager)
            )
            
            if hr >= 0:
                self.manager = manager
        except Exception as e:
            print(f"가상 데스크탑 관리자 초기화 실패: {e}")
    
    def is_window_on_current_desktop(self, hwnd):
        """창이 현재 가상 데스크탑에 있는지 확인"""
        try:
            if not self.manager:
                return True
                
            is_on_current = c_int()
            vtbl = self.manager.contents.lpVtbl.contents
            hr = vtbl.IsWindowOnCurrentVirtualDesktop(self.manager, hwnd, byref(is_on_current))
            return hr >= 0 and is_on_current.value
            
        except Exception as e:
            print(f"가상 데스크탑 확인 실패: {e}")
            return True 