

import paramiko
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def compress_pnx_via_bz(pnx):
    import inspect
    import os
    import re
    import shutil
    import traceback

    from datetime import datetime
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    try:
        while 1:
            ment = rf"백업 {pnx}"
            logging.debug(f" {ment}", )

            # 전처리
            pnx = pnx.replace("\n", "")
            pnx = pnx.replace("\"", "")

            if pnx.strip() == "":
                ensure_spoken(text="백업할 대상이 입력되지 않았습니다")
                break

            target_dirname = os.path.dirname(pnx)
            target_dirname_dirname = os.path.dirname(target_dirname)
            target_basename = os.path.basename(pnx).split(".")[0]
            target_zip = rf'{target_dirname}\$zip_{target_basename}.zip'
            target_yyyy_mm_dd_hh_mm_ss_zip_basename = rf'{target_basename} - {get_pk_time_2025_10_20_1159("%Y %m %d %H %M %S")}.zip'
            logging.debug(f"pnx : {pnx}")
            logging.debug(f"target_dirname : {target_dirname}")
            logging.debug(f"target_dirname_dirname : {target_dirname_dirname}")
            logging.debug(f"target_basename : {target_basename}")
            logging.debug(f"target_zip : {target_zip}")
            logging.debug(f"target_yyyy_mm_dd_HH_MM_SS_zip_basename : {target_yyyy_mm_dd_hh_mm_ss_zip_basename}")

            cmd = f'bz.exe c "{target_zip}" "{pnx}"'
            ensure_command_executed(cmd=cmd)

            cmd = rf'ren "{target_zip}" "{target_yyyy_mm_dd_hh_mm_ss_zip_basename}"'
            ensure_command_executed(cmd=cmd)

            # f이 위치한 드라이브로 이동
            drives = [
                "C",
                "D",
                "E",
                "F",
                "G",
            ]
            drive_where_target_is_located = pnx.split(":")[0].upper()
            for drive in drives:
                if (drive_where_target_is_located == drive):
                    os.system(rf"cd {drive}:")
            try:
                os.chdir(target_dirname)
            except:
                ensure_spoken(text="경로를 이해할 수 없습니다")
                os.chdir(d_pk_root)
                break
            lines = ensure_command_executed_like_human_as_admin('dir /b /a-d *.zip')
            print_magenta(rf'''len(lines)={len(lines)}''')
            for line in lines:
                print_magenta(f'''line={line}''')
                if line != "":
                    if os.getcwd() != line:  # 여기 os.getcwd() 이게 들어가네... 나중에 수정하자
                        # 2023-12-04 월 12:14 SyntaxWarning: invalid escape sequence '\d'
                        # r 을 사용 Raw String(원시 문자열),  \를 모두 remove
                        # 정규식은 r 쓰면 안된다. \ 써야한다?.
                        # 2023-12-12 화 14:23 SyntaxWarning: invalid escape sequence '\d'
                        # virtual environment 재설치 후 또 문제가 나타남,
                        # pattern='d{4} d{2} d{2} d{2} d{2} d{2}'
                        # pattern=r'\d{4} \d{2} \d{2} \d{2} \d{2} \d{2}'
                        pattern = r'd{4} d{2} d{2} d{2} d{2} d{2}'
                        # logging.debug(line)
                        if is_pattern_in_prompt(line, pattern):
                            logging.debug(f"zip f 목록에 대하여 {pattern} 타임스탬프 정규식 테스트를 통과했습니다")
                            # logging.debug(line)
                            # 2023-12-03 일 20:03 trouble shooting 성공
                            # 백업 시 타임스탬프에 언더바 넣도록 변경했는데 regex 는 변경 하지 않아서 난 실수 있었음.
                            time_to_backed_up = re.findall(pattern, line)
                            time_to_backed_up_ = time_to_backed_up[0][0:10].replace(" ", "-") + " " + time_to_backed_up[
                                                                                                          0][
                                                                                                      11:16].replace(
                                " ", ":") + ".00"
                            time_to_backed_up__ = datetime.strptime(str(time_to_backed_up_), '%Y-%m-%d %H:%M.%S')
                            time_current = datetime.now()
                            try:
                                target_dirname_old = rf'{target_dirname}\.pk_system'
                                if not os.path.exists(target_dirname_old):
                                    os.makedirs(target_dirname_old)
                            except Exception:
                                logging.debug(f'''{traceback.format_exc()}  ''',
                                         print_color='yellow')
                                os.chdir(d_pk_root)
                                break
                            # 지금부터 7일 이전의 f만
                            # diff=time_to_backed_up__ - time_current
                            # if diff.days <-7:
                            # logging.debug(f"line : {line}")

                            # logging.debug(f"1분(60 seconds) 이전의 f자동정리 시도...")
                            logging.debug(f"f자동정리 시도...")
                            change_min = time_current - datetime.timedelta(seconds=60)
                            diff = time_to_backed_up__ - change_min
                            if 60 < diff.seconds:
                                try:
                                    file_with_time_stamp_zip = os.path.abspath(line.strip())
                                    file_dirname_old_abspath = os.path.abspath(target_dirname_old)
                                    logging.debug(rf'move "{file_with_time_stamp_zip}" "{file_dirname_old_abspath}"')
                                    shutil.move(file_with_time_stamp_zip, file_dirname_old_abspath)
                                except Exception:
                                    logging.debug(f'''{traceback.format_exc()}  ''',
                                             print_color='yellow')
                                    os.chdir(d_pk_root)
                                    break
            os.chdir(d_pk_root)
            logging.debug(f" green {ment}")
            break
    except:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
        os.chdir(d_pk_root)
