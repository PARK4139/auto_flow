import random
import platform
import subprocess
import shutil
from pathlib import Path


def get_diet_type(item: str) -> str:
    VEGETABLES = ["오이무침", "시금치", "콩나물국", "방울토마토", "브로콜리찜", "숙주나물", "구운 가지", "가지나물", "청경채겉절이", "참나물무침", "우엉조림", "열무된장무침", "도라지나물", "상추쌈", "깻잎나물", "미역오이냉국", "나박김치", "무생채", "김 소량", "배추겉절이", "미나리무침", "양배추찜", "배추김치", "깍두기", "오이/당근스틱", "저염 채소죽", "삶은 브로콜리", "두부샐러드"]
    PROTEINS = ["두부부침", "닭가슴살샐러드", "고등어구이", "삶은 달걀", "무당 요거트", "돼지안심 채소볶음", "순두부찌개", "닭가슴살찜", "연어구이", "두부조림", "병아리콩 샐러드", "코다리찜", "닭가슴살구이", "조기구이", "두부채소볶음", "삶은 오징어", "콩비지찌개", "소고기무국", "된장국", "버섯된장국", "북어국", "미역국"]
    CARBS = ["현미밥", "보리밥", "잡곡밥", "귀리밥", "통밀토스트", "오트밀", "아몬드", "블루베리", "통밀빵", "사과 반쪽", "삶은 고구마", "아보카도", "저지방 우유", "무가당 두유"]

    if item in VEGETABLES:
        return "채소"
    elif item in PROTEINS:
        return "단백질"
    elif item in CARBS:
        return "탄수화물"
    else:
        return "기타"


def sort_items_by_type(items):
    return sorted(items, key=lambda x: {
        "채소": 0,
        "단백질": 1,
        "탄수화물": 2,
        "기타": 3
    }[get_diet_type(x)])


def open_file(path: Path) -> None:
    """Open the given file in platform-appropriate file browser."""
    abs_path = path.resolve()

    # WSL (detect 'microsoft' in release)
    if "microsoft" in platform.uname().release.lower():
        try:
            win_path = subprocess.check_output(["wslpath", "-w", str(abs_path)], text=True).strip()
            subprocess.Popen(["explorer.exe", win_path])
        except Exception as e:
            print(f"⚠️ 파일 열기 실패(WSL): {e}")
    elif platform.system() == "Linux" and shutil.which("xdg-open"):
        subprocess.Popen(["xdg-open", str(abs_path)])
    elif platform.system() == "Windows":
        subprocess.Popen(["explorer.exe", str(abs_path)])


def contains_any(item_list, keywords):
    """Return True if any of *keywords* appears (substring) in any element of *item_list*."""
    return any(kw in itm for itm in item_list for kw in keywords)


def ensure_diabetes_diet_consumed():
    # === [설정 시작] ===
    INCLUDE = ["두부"]
    EXCLUDE = [
        "흰쌀", "흰빵", "설탕", "시럽", "케이크", "과자", "탄산", "주스",
        "튀김", "삼겹살", "버터", "마가린", "햄", "소시지", "라면", "인스턴트",
        "술", "당절임", "패스트푸드", "바나나", "포도", "참외"
    ]

    RANDOM_MEAL_RANGE = (3, 3)  # 하루 3끼 고정

    from pk_internal_tools.pk_objects.pk_directories import D_LOGS
    OUTPUT_FILE = Path(D_LOGS) / "pk_chat.log"
    # === [설정 끝] ===

    SNACK_OPTIONS = [
        "삶은 고구마 소량", "방울토마토 + 아몬드", "호두 4알", "무가당 요거트 + 베리류",
        "사과 1/2개", "통밀 크래커 + 무가당 두유", "오이/당근스틱 + 허머스"
    ]

    diet_plan = {
        "월": {
            "아침": ["현미밥", "두부부침", "미역국", "오이무침"],
            "점심": ["보리밥", "닭가슴살샐러드", "된장국", "배추김치"],
            "저녁": ["잡곡밥", "고등어구이", "데친 시금치", "콩나물국"],
        },
        "화": {
            "아침": ["삶은 달걀", "통밀토스트", "방울토마토", "무당 요거트"],
            "점심": ["귀리밥", "돼지안심 채소볶음", "나박김치", "깻잎나물"],
            "저녁": ["현미밥", "순두부찌개", "브로콜리찜", "숙주나물"],
        },
        "수": {
            "아침": ["오트밀", "무가당 두유", "아몬드", "블루베리"],
            "점심": ["잡곡밥", "닭가슴살찜", "무생채", "된장깻잎"],
            "저녁": ["보리밥", "연어구이", "구운 가지", "미역오이냉국"],
        },
        "목": {
            "아침": ["삶은 고구마", "삶은 달걀", "오이/당근스틱", "아보카도"],
            "점심": ["현미밥", "두부조림", "배추겉절이", "버섯된장국"],
            "저녁": ["귀리밥", "우엉조림", "참나물무침", "북어국"],
        },
        "금": {
            "아침": ["병아리콩 샐러드", "통밀빵", "저지방 우유"],
            "점심": ["현미밥", "코다리찜", "양배추찜", "깍두기"],
            "저녁": ["잡곡밥", "닭가슴살구이", "미나리무침", "콩비지찌개"],
        },
        "토": {
            "아침": ["두부샐러드", "삶은 달걀", "사과 반쪽"],
            "점심": ["보리밥", "소고기무국", "상추쌈", "도라지나물"],
            "저녁": ["현미밥", "조기구이", "열무된장무침", "가지나물"],
        },
        "일": {
            "아침": ["저염 채소죽", "삶은 달걀", "삶은 브로콜리"],
            "점심": ["귀리밥", "된장찌개", "청경채겉절이", "삶은 오징어"],
            "저녁": ["현미밥", "두부채소볶음", "숙주된장국", "김 소량"],
        },
    }

    header = """당뇨 식단을 튜토리얼 하겠습니다.
1. 규칙적인 식사  하루 3끼 + 필요 시 간식(1~2회)  /  식사시간 일정하게 유지
2. 탄수화물 조절   과도한 밥·빵·면·떡 금지  /  현미·잡곡밥 등 복합 탄수화물, GI 낮은 탄수화물
3. 단백질 충분히   살코기·두부·계란·생선·콩류  (근육 유지, 혈당 조절)
4. 채소 풍부하게   식이섬유로 혈당 급상승 억제  (단, 당근·옥수수·고구마 조절)
5. 좋은 지방 위주  튀김·포화지방 피하고  올리브유·견과·아보카도·생선기름 OK
6. 과일은 소량     사과·베리·자몽 등 저당 과일  (1회 1/2개 정도)  /  바나나·포도·참외 피하기
7. 가공·단순당 금지  탄산·과자·빵·시리얼·라면·햄·패스트푸드·술 제한

🍱 하루 예시
아침  현미밥½ + 달걀찜 + 두부구이 + 채소무침 + 저지방 우유
점심  보리밥 + 닭가슴살샐러드 + 된장국 + 김치 소량
저녁  잡곡밥 + 연어구이 + 데친 브로콜리 + 미역국
간식  삶은 고구마 소량 / 방울토마토 + 호두 몇 알

음식 순서: 채소 → 단백질 → 탄수화물  (혈당 급등 억제)"""

    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    output_lines = [header, PK_UNDERLINE]

    for day, meals in diet_plan.items():
        output_lines.append(f"\n\n📅 {day}요일 식단")
        meal_order = ["아침", "점심", "저녁"]
        meal_time_map = {"아침": "07:30", "점심": "12:30", "저녁": "18:30"}

        for meal_time in meal_order:
            items = meals.get(meal_time, [])
            # EXCLUDE 필터링
            items = [i for i in items if not contains_any([i], EXCLUDE)]
            sorted_items = sort_items_by_type(items)
            meal_time_str = meal_time_map.get(meal_time, "")
            output_lines.append(f"{meal_time}({meal_time_str}): {', '.join(sorted_items)}")

            # 간식 추가
            if meal_time == "아침":
                snack = random.choice(SNACK_OPTIONS)
                output_lines.append(f"오전 간식(10:00): {snack}")
            if meal_time == "점심":
                snack = random.choice(SNACK_OPTIONS)
                output_lines.append(f"오후 간식(15:00): {snack}")

        output_lines.append("섭취 순서: 채소 → 단백질 → 탄수화물\n")

    # 기존 파일 삭제
    if OUTPUT_FILE.exists():
        try:
            OUTPUT_FILE.unlink()
        except Exception:
            pass

    # 결과 저장
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(output_lines), encoding="utf-8")

    print(f"\n✅ 저장 완료: {OUTPUT_FILE}")
    open_file(OUTPUT_FILE)


if __name__ == "__main__":
    ensure_diabetes_diet_consumed()
