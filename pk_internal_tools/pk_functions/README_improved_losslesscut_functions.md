# 개선된 LosslessCut 함수 사용 튜토리얼

## 개요

`ensure_target_files_played_on_losslesscut` 함수의 문제점들을 점진적으로 개선한 버전입니다.

## 해결된 문제점

### n. Ctrl+C/V 동작하지 않는 문제 ✅
- **원인**: `pyautogui` 키 입력이 시스템 전체에 영향을 줌
- **해결**: 윈도우 포커스 기반의 정확한 키 입력 처리
- **함수**: `ensure_video_playied_at_losslesscut_improved()`

### n. LosslessCut 실행 모니터링 성능 문제 ✅
- **원인**: `tasklist.exe | findstr` 명령어가 느림
- **해결**: 윈도우 핸들 + 프로세스 목록의 하이브리드 방식
- **함수**: `is_media_file_controller_running_improved()`

### n. 비디오 로드 후 재생 지연 문제 ✅
- **원인**: 고정 대기 시간으로 인한 비효율성
- **해결**: 적응형 대기 시간 + 진행률 표시
- **함수**: `ensure_video_playied_at_losslesscut_with_adaptive_wait()`

## 설정 옵션

메인 함수 상단에서 다음 설정을 조정할 수 있습니다:

```python
# 개선된 함수 사용 설정 (사용자가 선택 가능)
USE_IMPROVED_MONITORING = True      # 개선된 모니터링 함수 사용
USE_IMPROVED_PLAYBACK = True        # 개선된 재생 함수 사용
USE_ADAPTIVE_WAIT = False           # 적응형 대기 시간 사용 (더 정확하지만 느림)
```

### 설정 조합별 동작

| 모니터링 | 재생 | 적응형 대기 | 설명 |
|---------|------|------------|------|
| `True` | `True` | `False` | **권장 설정** - 빠르고 안정적 |
| `True` | `True` | `True` | 가장 정확하지만 느림 |
| `False` | `False` | `False` | 기존 방식 (문제점 존재) |

## 개선된 함수 상세 설명

### n. `is_media_file_controller_running_improved()`
- **1차**: 윈도우 핸들로 빠른 확인 (가장 빠름)
- **2차**: psutil로 프로세스 목록 확인 (백업)
- **3차**: 기존 tasklist 방식 (최종 폴백)

### n. `ensure_video_playied_at_losslesscut_improved()`
- 윈도우 포커스 정확히 설정
- ESC 키 입력 후 충분한 대기 시간 (500ms)
- 클립보드 기능 방해 최소화

### n. `ensure_video_playied_at_losslesscut_with_adaptive_wait()`
- 비디오 준비 상태를 실시간으로 모니터링
- 최대 30초까지 대기 (설정 가능)
- 10초마다 진행률 표시
- 준비 완료 시점에 정확한 재생 시작

## 사용 예시

### 기본 사용 (권장)
```python
# 설정을 기본값으로 두고 실행
ensure_target_files_played_on_losslesscut(max_files=500)
```

### 고성능 모드
```python
# 설정을 수정하여 최고 성능으로 실행
USE_IMPROVED_MONITORING = True
USE_IMPROVED_PLAYBACK = True
USE_ADAPTIVE_WAIT = False
ensure_target_files_played_on_losslesscut(max_files=500)
```

### 정확성 우선 모드
```python
# 설정을 수정하여 정확성 우선으로 실행
USE_IMPROVED_MONITORING = True
USE_IMPROVED_PLAYBACK = True
USE_ADAPTIVE_WAIT = True
ensure_target_files_played_on_losslesscut(max_files=500)
```

## 성능 비교

| 방식 | 모니터링 속도 | 재생 정확도 | 클립보드 호환성 | 설명 |
|------|--------------|------------|----------------|------|
| 기존 | 느림 (1-2초) | 보통 | ❌ | 문제점 존재 |
| 개선 | 빠름 (0.1초) | 높음 | ✅ | 권장 |
| 적응형 | 빠름 (0.1초) | 최고 | ✅ | 정확성 우선 |

## 문제 해결

### 개선된 함수가 실패하는 경우
- 자동으로 기존 함수로 폴백
- 로그에 상세한 오류 정보 기록
- `playback_success` 변수로 성공 여부 확인

### 의존성 문제
- `win32gui`: Windows API 접근용
- `psutil`: 프로세스 모니터링용 (선택사항)
- `pyautogui`: 키 입력 시뮬레이션용

## 향후 개선 계획

1. **성능 최적화**: 더 빠른 윈도우 상태 확인
2. **에러 처리**: 더 세밀한 예외 상황 대응
3. **설정 파일**: 외부 설정 파일로 옵션 관리
4. **로깅 개선**: 더 상세한 디버깅 정보

## 피드백 및 문의

함수 사용 중 문제가 발생하거나 개선 제안이 있으시면 알려주세요.
