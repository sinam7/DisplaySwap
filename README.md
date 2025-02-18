# DisplaySwap

DisplaySwap은 Windows 10에서 듀얼 모니터 간 창을 쉽게 교환할 수 있는 도구입니다. 가상 데스크톱을 지원하여 현재 활성화된 가상 데스크톱의 창만 교환합니다.

## 특징

- Windows + ` 단축키로 간편한 창 교환
- 가상 데스크톱 지원 (현재 데스크톱의 창만 교환)
- 최대화된 창 지원
- 시스템 트레이 아이콘으로 편리한 관리
- 관리자 권한으로 실행하여 모든 창 제어 가능

## 테스트 환경

- Windows 10
- 듀얼 모니터 (각각 1920x1080)
- 가로 배치 (좌우 배치)

## 설치

1. 최신 릴리즈에서 설치 파일 다운로드
2. 관리자 권한으로 실행

또는 소스에서 직접 빌드:

~~~bash
# 1. 저장소 클론
git clone https://github.com/your-username/DisplaySwap.git
cd DisplaySwap

# 2. 가상환경 생성 및 활성화
python -m venv venv
.\venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 빌드
python setup.py build
~~~

## 사용법

1. 프로그램 실행 (관리자 권한 필요)
2. Windows + ` 키를 눌러 현재 가상 데스크톱의 창들을 교환
3. 시스템 트레이의 DisplaySwap 아이콘으로 프로그램 관리
   - 우클릭으로 메뉴 열기
   - "종료" 선택으로 프로그램 종료

## 주의사항

- 관리자 권한이 필요합니다 (일부 창 제어를 위해)
- 일부 UWP 앱은 제어가 제한될 수 있습니다
- 현재 가상 데스크톱의 창만 교환됩니다

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요. 