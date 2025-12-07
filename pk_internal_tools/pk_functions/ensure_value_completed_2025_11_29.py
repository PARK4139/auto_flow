from pk_internal_tools.pk_objects.pk_fzf_theme import PkFzfTheme
                                                                                    
def ensure_value_completed_2025_11_29(file_id, editable, options, query="", guide_text=None
, fzf_theme: PkFzfTheme = PkFzfTheme(), multi_select: bool = False):
    import logging                                                                  
    import os                                                                       
    import platform                                                                 
    import subprocess                                                               
    import tempfile                                                                 
    import textwrap                                                                 
    import traceback                                                                
                                                                                    
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import
ensure_debug_loged_verbose                                                          
    from pk_internal_tools.pk_functions.get_prompt_label import get_prompt
_label                                                                              
    from pk_internal_tools.pk_functions.get_prompt_label_guide_text import
 get_prompt_label_guide_text                                                        
    from pk_internal_tools.pk_functions.get_window_title_temp import get_w
indow_title_temp                                                                    
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_files import F_ENSURE_ARG_RECIEVE
D                                                                                   
    from pk_internal_tools.pk_objects.pk_files import F_PK_ENSURE_GEMINI_C
LI_LOCATED_TO_FRONT, F_PK_ENSURE_GEMINI_CLI_INITIAL_PROMPT_LOADED_PY            
    from pk_internal_tools.pk_objects.pk_etc import pk_HEX_COLOR
_MAP                                                                                
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_
made                                                                                
    from pk_internal_tools.pk_functions.get_str_removed_bracket_hashed_prefix import get_str_removed_bracket_hashed_prefix
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import en
sure_pnx_opened_by_ext                                                              
    from pk_internal_tools.pk_functions.ensure_value_advanced_fallback_via
_input import ensure_value_advanced_fallback_via_input                              
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensu
re_window_to_front                                                                  
    from pk_internal_tools.pk_functions.get_f_historical import get_histor
y_file_path                                                                         
    from pk_internal_tools.pk_functions.get_fzf_command import get_fzf_com
mand                                                                                
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_l
linux                                                                                
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_sens
itive                                                                               
    from pk_internal_tools.pk_objects.pk_etc import PK_BLANK
                                                                                    
    ensure_pnx_made(pnx=d_pk_root_hidden, mode="f")                              
                                                                                    
    history_file = get_history_file_path(file_id=file_id)                           
    if editable is True:                                                            
        ensure_pnx_opened_by_ext(pnx=history_file)                                  
        ensure_window_to_front(get_nx(history_file))                                
                                                                                    
    fzf_temp_file = None                                                            
    selected_value = None                                                           
    try:                                                                            
                                                                                    
        # n. 옵션 임시 파일  # len(cmd) 가 길면 win                                 
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', n
ewline="\n") as temp_f:
            temp_f.write("\n".join(options))
            fzf_temp_file = temp_f.name                                             
                                                                                    
        # fzf 경로 확보 및 문자열화                                                 
        fzf_cmd = get_fzf_command()                                                 
        logging.debug(rf"fzf_cmd={fzf_cmd}")                                        
        fzf_cmd = str(fzf_cmd) if fzf_cmd else None                                 
        if not fzf_cmd:                                                             
            return ensure_value_advanced_fallback_via_input(options, query)         
                                                                                    
        # OS별 커맨드들                                                             
        opening_command = 'xdg-open "{}"'
        copy_command = "xclip -selection clipboard"
        fzf_preview_option = 'bat --style=numbers --color=always "{}"'
                                                                                    
        def is_os_macos():                                                          
            return platform.system().lower() == "darwin"                            
                                                                                    
        if is_os_windows():                                                         
            # opening_command = 'start "" explorer.exe "{}"' # fail                 
            # opening_command = 'start "" explorer.exe "{{}}"' # fail               
            # opening_command = 'start "" explorer.exe "{{}}"'                      
            copy_command = 'clip.exe'                                               
            fzf_preview_option = 'type "{}"'
        elif is_os_wsl_linux():                                                     
            opening_command = 'explorer.exe "{}"'
            copy_command = 'clip.exe'                                               
            fzf_preview_option = 'bat --style=numbers --color=always "{}"'
        elif is_os_macos():                                                         
            opening_command = 'open "{}"'
            copy_command = 'pbcopy'
            fzf_preview_option = 'cat "{}"'
                                                                                    
        # 4) 너무 긴 초기 query 컷 (명령행/렌더 성능 보호)                          
        SAFE_QUERY_MAX = 512                                                        
        if query and len(query) > SAFE_QUERY_MAX:                                   
            logging.warning(f"[WARN] query too long ({{len(query)}}), truncated to {
SAFE_QUERY_MAX}")                                                                   
            query = query[:SAFE_QUERY_MAX]                                          
                                                                                    
        bind_entries = [                                                            
            "tab:down",                                                             
            "shift-tab:up",                                                             
            f'ctrl-o:select+execute-silent(cmd /k echo {{}} | python "{F_ENSURE_ARG_
RECIEVED}" --from-stdin)',                                                          
            f"ctrl-y:execute-silent(echo {{}} | {copy_command})",                   
            "ctrl-p:toggle-preview",                                                
            "ctrl-k:kill-line",                                                     
                                                                                    
            "alt-d:page-down",  # Alt+d : 한 화면 아래                              
            "alt-u:page-up",  # Alt+u : 한 화면 위                                  
            "alt-D:half-page-down",  # Alt+Shift+d                                  
            "alt-U:half-page-up",  # Alt+Shift+u                                    
            "alt-a:select-all", # ALT+A to select all                               
                                                                                    
            f'alt-`:execute(cmd /k start "{get_window_title_temp()}" "{history_file}
"',                                                                                
                                                                                    
            f'ALT-1:execute(start "{get_window_title_temp()}" python "{F_PK_ENSURE_G
EMINI_CLI_WHIP_KIT_ENABLED_INTERACTIVE})',                                          
            f'ALT-2:execute(start "{get_window_title_temp()}" python "{F_PK_ENSURE_G
EMINI_CLI_LOCATED_TO_FRONT})',                                                      
        ]                                                                           
                                                                                    
        def add_binds(cmd_list, entries, max_len=1500):                             
            # 한 인자에 몰아넣지 않도록 길이 기준으로 분할                          
            chunk = []                                                              
            length = 0                                                              
            for be in entries:                                                      
                add = ("," if chunk else "") + be                                   
                if length + len(add) > max_len:                                     
                    cmd_list += ["--bind", ",".join(chunk)]                         
                    chunk, length = [be], len(be)                                   
                else:                                                               
                    chunk.append(be)                                                
                    length += len(add)                                              
            if chunk:                                                               
                cmd_list += ["--bind", ",".join(chunk)]                             
            return cmd_list                                                         
                                                                                    
        # 프롬프트/풋터 (개행 금지)                                                 
        prompt_label = get_prompt_label(file_id)                                    
        prompt_label_guide_text = get_prompt_label_guide_text(prompt_label)         
                                                                                    
        footer_text = None                                                          
        footer_text_color = None                                                    
        shourtcut_guide_text_default = textwrap.dedent(rf'''                        
            # 단축키 {PkTexts.GUIDE}                                                
            CTRL-O: 열기                                                            
            CTRL-Y: 복사                                                            
            CTRL-P: 프리뷰 토글                                                     
            CTRL-K: 커서의 뒤 삭제                                                  
            CTRL-U: 커서의 앞 삭제                                                  
            CTRL-A: 커서를 앞으로 이동(줄끝 단위)                                   
            CTRL-E: 커서를 뒤로 이동(줄끝 단위)                                     
            ALT-B: 커서를 앞으로 이동(단어 단위)                                    
            ALT-F: 커서를 뒤로 이동(단어 단위)                                      
            ALT-A: 모든 항목 선택/선택 해제 (멀티 선택 모드에서)                    
                                                                                    
            # 사용자 입력 {PkTexts.GUIDE}                                           
            {prompt_label_guide_text}                                               
        ''')                                                                        
        if guide_text is None:                                                      
            footer_text = shourtcut_guide_text_default                              
            footer_text_color = PK_HEX_COLOR_MAP["WHITE"]                           
        else:                                                                       
            footer_text_color = PK_HEX_COLOR_MAP["YELLOW"]                          
            footer_text = guide_text                                                
                                                                                    
        cmd = [fzf_cmd, "--print-query"]                                            
        if query:                                                                   
            cmd += ["--query", query]                                               
                                                                                    
        if multi_select: # Add --multi option if multi_select is True               
            cmd += ["--multi"]                                                      
                                                                                    
        cmd += [                                                                    
            "--no-mouse",                                                           
            f"--prompt={prompt_label}={PK_BLANK}{PK_BLANK}",                        
            "--pointer=▶",                                                          
            f"--color=prompt:#ffffff,pointer:#4da6ff,hl:#3399ff,hl+:#3399ff,fg+:#339
9ff,footer:{footer_text_color}",                                                    
            "--footer", footer_text,                                                
            # "--height=90%", "--layout=reverse",                                   
        ]                                                                           
        if fzf_theme.layout_reverse:                                                
            cmd.append("--layout=reverse")                                          
        if fzf_theme.border_style is not None:                                      
            if fzf_theme.border_style == "":                                        
                cmd.append("--border")                                              
            else:                                                                   
                cmd.append(f"--border={fzf_theme.border_style}")                    
                                                                                    
        cmd = add_binds(cmd, bind_entries)                                          
                                                                                    
        # 최종 커맨드라인 길이 경고                                                 
        try:                                                                        
            from subprocess import list2cmdline                                     
            cmdline_preview = list2cmdline(cmd)                                     
            if len(cmdline_preview) > 7000:                                         
                logging.warning(f"{PkTexts.WARNING} fzf command line length={len(cmd
line_preview)} (>7000)")                                                            
        except Exception:                                                           
            pass                                                                    
                                                                                    
        # 디버그                                                                    
        logging.debug(rf"cmd={cmd}")                                                
                                                                                    
                                                                                    
        # 실행 (대화형 유지용: stdin=파일핸들, stdout=PIPE 허용 — fzf UI 정상 동작) 
        with open(fzf_temp_file, 'r', encoding='utf-8') as stdin_file:              
            proc = subprocess.Popen(                                                
                cmd,                                                                
                stdin=stdin_file,                                                   
                stdout=subprocess.PIPE,                                             
                stderr=subprocess.PIPE,                                             
                text=True,                                                          
                encoding='utf-8',                                                   
                shell=False,                                                        
            )                                                                       
            out, err = proc.communicate()                                           
                                                                                    
        if proc.returncode not in (0, 130):                                         
            logging.error(f"fzf exited with code {proc.returncode}, stderr={{(err or 
'').strip()}}")                                                                      
                                                                                    
        # 결과 파싱                                                                 
        out = (out or "").strip()                                                   
        lines = out.split("\n") if out else []                                      
        query_out = lines[0] if len(lines) > 0 else ""                              
        selection_lines = lines[1:] if len(lines) > 1 else []                       
                                                                                    
        if multi_select:                                                            
            selected_values = [get_str_removed_bracket_hashed_prefix(s).strip() for s in s
election_lines if s.strip()]                                                        
        else:                                                                       
            selected_value = selection_lines[0] if selection_lines else ""          
            selected_values = [get_str_removed_bracket_hashed_prefix(selected_value).strip
()] if selected_value else []                                                       
                                                                                    
        # 로그 포맷 버그 수정 (삼중따옴표 중첩 제거)                                
        logging.debug(f"selected_values={{selected_values}} ") # Changed to selected_v
alues for multi_select                                                              
                                                                                    
        if not selected_values:                                                     
            logging.debug("Selection was cancelled.")                               
            return [] # Return empty list for multi_select                          
                                                                                    
        return selected_values[0] if not multi_select else selected_values # Return 
first element if not multi_select, else list                                        
    except:                                                                         
        ensure_debug_loged_verbose(traceback)                                       
        selected_value = ensure_value_advanced_fallback_via_input(options, query)   
        return selected_value                                                       
    finally:                                                                        
        if fzf_temp_file and os.path.exists(fzf_temp_file):                         
            try:                                                                    
                os.remove(fzf_temp_file)                                            
            except:                                                                 
                ensure_debug_loged_verbose(traceback)                               
                                                                                    
    # 가드(프로텍트 코드)                                                           
    if not multi_select and selected_value not in options: # selected_value needs to
 be defined if not multi_select                                                     
        if not selected_value: # handle case where selected_value is empty string fo
r single select                                                                     
            logging.warning("No value selected for single select.")                 
            return None                                                             
        logging.warning(f"Entered value is not in the option list: {selected_value}"
)                                                                                   
    return selected_value
