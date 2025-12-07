from pk_internal_tools.pk_functions.get_nx import get_nx
import logging
from pathlib import Path


def compare_target_tree(f_target_tree_answer_list, f_target_ref_tree2_list, ignore_list):
    """
    두 TOML f의 tree.paths를 비교하여 추가된 f과 remove된 f 출력
    :param f_ref: 기준이 되는 TOML f 경로
    :param f_path_list_measured: 측정된 TOML f 경로
    :param ignore_list: 비교에서 제외할 경로들의 리스트
    """
    f_target_tree_answer_list = Path(f_target_tree_answer_list)

    if ignore_list is None:
        ignore_list = []

    # 기준 및 측정된 경로 가져오기
    ref_paths = set(get_data_from_f_toml(f_target_tree_answer_list)["tree"]["paths"])
    measured_paths = set(get_data_from_f_toml(f_target_ref_tree2_list)["tree"]["paths"])

    # 경로가 ignore_list의 항목을 포함하는지 확인
    def should_ignore(path):
        return any(ignored in path for ignored in ignore_list)

    # ignore_list 에 포함된 항목 remove
    ref_paths = {path for path in ref_paths if not should_ignore(path)}
    measured_paths = {path for path in measured_paths if not should_ignore(path)}

    # 추가된 f과 remove된 f 추출
    added_files = list(measured_paths - ref_paths)
    removed_files = list(ref_paths - measured_paths)

    # 추가된 f 출력
    logging.debug(
        f"{"[ INFO ]"} {get_nx(f_target_ref_tree2_list)} 에 추가된 f (+{len(added_files)} EA) : 참고 : ({get_nx(f_target_tree_answer_list)}[원격지_f_]와 {get_nx(f_target_ref_tree2_list)}[로컬_f_]의 트리비교)",
        print_color='blue')
    for file in sorted(added_files):
        logging.debug(file)

    # 누락된 f 출력
    # 누락 파악이 더 중요.
    logging.debug(
        f"{"[ ERROR ]"} {get_nx(f_target_ref_tree2_list)} 에서 누락된 f (-{len(removed_files)} EA) : 참고 : ({get_nx(f_target_tree_answer_list)}[원격지_f_]와 {get_nx(f_target_ref_tree2_list)}[로컬_f_]의 트리비교)",
        print_color='yellow')
    for file in sorted(removed_files):
        logging.debug(f"{file}")
    if len(removed_files) == 0:
        logging.debug(f"{"[ SUCCEEDED ]"} {get_nx(f_target_ref_tree2_list)} 에서 누락된 f이 없습니다 : 참고 : ({get_nx(f_target_tree_answer_list)}와 {get_nx(f_target_ref_tree2_list)}의 트리비교)",
            print_color='green')
