
def count_down(countdown_limit_upper):  #
    for i in range(0, countdown_limit_upper, -1):
        logging.debug_and_speak(f'count down {i}')