from cx_Freeze import setup, Executable
import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        'display_swap.py',
        base=base,
        uac_admin=True,  # UAC 프롬프트 활성화
        manifest='manifest.xml',
        target_name='DisplaySwap.exe',  # 실행 파일 이름
        icon='icon.ico'  # 아이콘 추가 (선택사항)
    )
]

# MSI 설치 프로그램에 대한 추가 옵션
build_options = {
    "includes": [],
    "packages": [
        "keyboard", "win32gui", "win32con", "win32api", 
        "ctypes", "comtypes", "PIL", "pystray"
    ],
    "include_files": ["manifest.xml", "icon.ico"],
}

setup(
    name="DisplaySwap",
    version="1.0.2",
    description="Display Window Swap Tool",
    options={
        "build_exe": build_options,
    },
    executables=executables
) 