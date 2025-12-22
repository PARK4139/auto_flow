def get_list_calculated(origin_list, minus_list=None, plus_list=None, dedup=True):
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    origin_list = origin_list or []
    minus_list = minus_list or []
    plus_list = plus_list or []
    print_limit = min(len(origin_list), len(minus_list), len(plus_list))
    # if QC_MODE:
    #     logging.debug(f'''print_limit={print_limit} ''')
    #     logging.debug(f'''len(origin_list)={len(origin_list)} ''')
    #     logging.debug(f'''len(minus_list)={len(minus_list)} ''')
    #     logging.debug(f'''len(plus_list)={len(plus_list)} ''')

    if dedup:
        seen_normalized = set()
        result = []

        def normalize(item):
            return str(item).strip().lower()

        # Process origin_list
        for x in origin_list:
            normalized_x = normalize(x)
            is_in_minus_list = False
            for item_in_minus_list in minus_list:
                if normalize(item_in_minus_list) == normalized_x:
                    is_in_minus_list = True
                    break
            
            if not is_in_minus_list and normalized_x not in seen_normalized:
                seen_normalized.add(normalized_x)
                result.append(x)

        # Process plus_list
        for x in plus_list:
            normalized_x = normalize(x)
            if normalized_x not in seen_normalized:
                seen_normalized.add(normalized_x)
                result.append(x)

        if QC_MODE:
            logging.debug(f'''len(result)={len(result)} ''')
        return result
    else:
        minus_set = set(minus_list)
        result = [x for x in origin_list if x not in minus_set]
        result.extend(plus_list)
        if QC_MODE:
            logging.debug(f'''len(result)={len(result)} ''')
        return result
