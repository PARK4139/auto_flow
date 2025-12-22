def print_f_list_preview(files, num_preview=10):
    """수집될 파일 목록을 미리보기로 출력"""
    print(f"총 {len(files)}개 항목 중 앞{num_preview}개:")
    for path in files[:num_preview]:
        print(" pk_?? ", path)
    if len(files) > num_preview:
        print("...")
