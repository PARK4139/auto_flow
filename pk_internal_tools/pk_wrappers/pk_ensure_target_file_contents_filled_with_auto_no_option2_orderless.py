import browser_cookie3







def pk_ensure_target_file_contents_filled_with_auto_no_option2_orderless(contents: str, unique_word: str, auto_cnt_starting_no=0):
    import inspect
    import re
    func_n = get_caller_name()
    # logging.debug("항상 필요했던 부분인데 만들었다. 편하게 개발하자. //웹 서비스 형태로 아무때서나 접근이되면 더 좋을 것 같다.  웹 개발툴 을 만들어 보자")
    before = unique_word
    after = 0 + auto_cnt_starting_no
    contents_new = []
    # lines=contents.split("\n")
    lines = contents.strip().split("\n")  # 문제 없긴 했는데,  어떻게 되나 실험해보자 안되면 위의 코드로 주석 스와핑할것.
    for line in lines:
        # logging.debug(line)
        # logging.debug(before)
        # logging.debug(str(after))
        after = after + 1

        line_new = re.sub(str(before), str(after), str(line))
        # logging.debug(line_new)
        contents_new.append(line_new)

    # logging.debug("str list to str")
    delimiter = "\n"
    contents_new_as_str = delimiter.join(contents_new)
    return contents_new_as_str
