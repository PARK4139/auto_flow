# pk_system Language 관련 Circular Import 분석 보고서

**생성일**: 2025-11-25  
**분석 대상**: Language 관련 모듈들의 import 의존성

---

## 🔄 발견된 Circular Import 체인

### Circular Import #1: `pk_texts.py` ↔ `get_pk_language()`

#### 체인 상세:

```
pk_texts.py (라인 1537-1542)
  ↓ import (모듈 로드 시 즉시 실행)
get_pk_language()
  ↓ 호출
get_values_from_historical_file_routine()
  또는
get_values_from_historical_database_routine()
  ↓ 사용
get_value_from_fzf_routine() (필요시)
  ↓ import (라인 14)
pk_texts.PkTexts
  ↓ 
pk_texts.py (다시 돌아옴) ❌ CIRCULAR!
```

#### 문제점:

1. **`pk_texts.py` (라인 1536-1542)**:
   ```python
   try:
       from pk_internal_tools.pk_functions.get_pk_language import get_pk_language
       lang = get_pk_language()
       PkTexts.set_lang(lang)
   except Exception as e:
       PkTexts.set_lang("english")
   ```
   - 모듈이 로드될 때 **즉시** `get_pk_language()` 호출
   - 언어를 설정하기 위해 함수 실행

2. **`get_pk_language()`**:
   - `get_values_from_historical_file_routine()` 또는 `get_values_from_historical_database_routine()` 호출
   - 이 함수들이 필요시 `get_value_from_fzf_routine()` 호출

3. **`get_value_from_fzf_routine()` (라인 14)**:
   ```python
   from pk_internal_tools.pk_objects.pk_texts import PkTexts
   ```
   - `PkTexts`를 import하여 사용
   - 이 시점에 `pk_texts.py`가 아직 완전히 로드되지 않았을 수 있음

---

## 🔍 Circular Import #2: `pk_translation.py` ↔ `get_pk_language()`

#### 체인 상세:

```
pk_translation.py (라인 1)
  ↓ import
get_pk_language()
  ↓ 호출
get_values_from_historical_file_routine()
  또는
get_values_from_historical_database_routine()
  ↓ 사용
get_value_from_fzf_routine() (필요시)
  ↓ import
pk_texts.PkTexts
  ↓
pk_texts.py
  ↓ import (라인 1537)
get_pk_language()
  ↓
pk_translation.py (다시 돌아옴) ❌ CIRCULAR!
```

#### 문제점:

- `pk_translation.py`는 `get_pk_language`를 **상단에서 import**
- `pk_texts.py`도 모듈 로드 시 `get_pk_language` 호출
- 서로 간접적으로 의존

---

## 📝 관련 파일 목록

1. **`pk_internal_tools/pk_objects/pk_texts.py`**
   - 라인 1537: `get_pk_language()` 호출 (모듈 로드 시)

2. **`pk_internal_tools/pk_objects/pk_translation.py`**
   - 라인 1: `get_pk_language` import

3. **`pk_internal_tools/pk_functions/get_pk_language.py`**
   - `get_values_from_historical_file_routine()` 사용
   - `get_values_from_historical_database_routine()` 사용

4. **`pk_internal_tools/pk_functions/get_values_from_historical_file_routine.py`**
   - (간접적으로) `get_value_from_fzf_routine()` 사용 가능

5. **`pk_internal_tools/pk_functions/get_values_from_historical_database_routine.py`**
   - (간접적으로) `get_value_from_fzf_routine()` 사용 가능

6. **`pk_internal_tools/pk_functions/get_value_from_fzf_routine.py`**
   - 라인 14: `PkTexts` import

---

## ⚠️ 발생 가능한 문제

1. **ImportError 발생 가능성**:
   ```
   ImportError: cannot import name 'PkTexts' from partially initialized module 'pk_texts'
   ```

2. **언어 설정 실패**:
   - `PkTexts.set_lang()` 호출이 실패하여 기본값만 사용

3. **런타임 에러**:
   - 모듈 로드 순서에 따라 에러가 발생하거나 발생하지 않을 수 있음 (비결정적)

---

## 🔧 해결 방안

### 방안 1: Lazy Import 패턴 사용 (권장)

`pk_texts.py`에서 모듈 로드 시 즉시 실행 대신, 필요할 때만 언어를 설정:

```python
# pk_texts.py 수정 전 (현재)
try:
    from pk_internal_tools.pk_functions.get_pk_language import get_pk_language
    lang = get_pk_language()
    PkTexts.set_lang(lang)
except Exception as e:
    PkTexts.set_lang("english")

# 수정 후 (Lazy Import)
def _initialize_language():
    """언어 설정을 지연 초기화"""
    try:
        from pk_internal_tools.pk_functions.get_pk_language import get_pk_language
        lang = get_pk_language()
        PkTexts.set_lang(lang)
    except Exception as e:
        PkTexts.set_lang("english")

# 모듈 로드 시 기본값으로 초기화
PkTexts.set_lang("english")

# 실제 사용 시 언어 설정 (예: ensure_pk_system_log_initialized에서)
# _initialize_language() 호출
```

### 방안 2: `get_value_from_fzf_routine`에서 Lazy Import

`get_value_from_fzf_routine`에서 `PkTexts`를 함수 내부에서 import:

```python
# get_value_from_fzf_routine.py 수정
def get_value_from_fzf_routine(...):
    # 함수 내부에서 import (필요할 때만)
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    ...
```

이미 함수 내부에서 import하고 있으므로 이 부분은 문제 없음.

### 방안 3: `pk_translation.py`에서 Lazy Import

`pk_translation.py`에서 `get_pk_language`를 사용할 때만 import:

```python
# pk_translation.py 수정
class PkTranslation2025:
    # ... 기존 코드 ...
    
    @classmethod
    def get_language(cls):
        """언어를 lazy하게 가져옴"""
        from pk_internal_tools.pk_functions.get_pk_language import get_pk_language
        return get_pk_language()
```

---

## ✅ 권장 해결책

**방안 1 + 방안 3 조합**을 권장합니다:

1. `pk_texts.py`에서 모듈 로드 시 즉시 실행하는 대신, 함수로 분리
2. 언어 설정이 필요한 시점(예: `ensure_pk_system_log_initialized`)에서 호출
3. `pk_translation.py`에서도 필요할 때만 언어를 가져오도록 변경

이렇게 하면 circular import를 완전히 제거할 수 있습니다.

---

## 📎 참고 파일

- `pk_internal_tools/pk_objects/pk_texts.py` (라인 1536-1542)
- `pk_internal_tools/pk_objects/pk_translation.py` (라인 1)
- `pk_internal_tools/pk_functions/get_pk_language.py`
- `pk_internal_tools/pk_functions/get_value_from_fzf_routine.py` (라인 14)







