import dataclasses
from dataclasses import field
from typing import Optional, List

from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

from pk_internal_tools.pk_functions.ensure_sensitive_info_masked import ensure_sensitive_info_masked # Added for sensitive data masking

_PK_COLORS = PK_ANSI_COLOR_MAP
_RESET = PK_ANSI_COLOR_MAP['RESET']


@dataclasses.dataclass
class StockInfoItem:
    name: str
    code: Optional[str] = None
    price: str = "N/A"
    source_date: str = ""
    source: str = ""
    reason: Optional[str] = None
    comparison_value: Optional[str] = None
    comparison_score: Optional[str] = None


@dataclasses.dataclass
class PkInterestingInfos:
    """관심 정보를 담는 데이터 클래스"""
    date: str = ""
    time: str = ""
    day_of_week: str = ""
    location: str = ""
    weather_infos: List[str] = field(default_factory=list)
    stock_info: Optional[List[StockInfoItem]] = field(default_factory=list)
    os_info: Optional[str] = None
    window_titles: List[str] = field(default_factory=list)
    processes_info: List[str] = field(default_factory=list)
    tasklist_info: List[str] = field(default_factory=list)
    image_names_info: List[str] = field(default_factory=list)
    ai_ide_processes_info: List[str] = field(default_factory=list)
    top_cpu_processes: List[dict] = field(default_factory=list)
    top_memory_processes: List[dict] = field(default_factory=list)
    wifi_profile_name: Optional[str] = None
    wifi_password: Optional[str] = None
    python_imports_info: Optional[str] = None
    connected_drives_info: Optional[str] = None
    screen_info: Optional[str] = None
    project_info: Optional[str] = None
    lta: Optional[bool] = None

    def __str__(self):
        parts = []

        # n. 일반 컨텍스트 (context)
        if self.date:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}날짜:{_RESET} {self.date}"
            )
        if self.time:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}시간:{_RESET} {self.time}"
            )
        if self.day_of_week:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}요일:{_RESET} {self.day_of_week}"
            )
        if self.location:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}위치:{_RESET} {self.location}"
            )
        if self.weather_infos:
            # weather_infos 리스트의 모든 항목을 줄바꿈과 들여쓰기로 구분하여 추가
            weather_details = "\n".join([f"  - {info}" for info in self.weather_infos])
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}날씨 정보:{_RESET}\n{weather_details}"
            )

        # n. 디바이스 (device)
        if self.os_info:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}OS 정보:{_RESET} {self.os_info}"
            )
        if self.screen_info:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}화면 정보:{_RESET}\n"
                f"{self.screen_info}"
            )
        if self.connected_drives_info:
            formatted_drives_str = self._format_connected_drives_info(str(self.connected_drives_info))
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}연결된 드라이브 정보(C 드라이브 제외):{_RESET}\n"
                f"{formatted_drives_str}"
            )

        # 3. 네트워크 (network)
        if self.wifi_profile_name:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}WiFi 프로필명:{_RESET} {self.wifi_profile_name}"
            )
        if self.wifi_password:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}WiFi 비밀번호:{_RESET} {ensure_sensitive_info_masked(self.wifi_password)}"
            )

        # 4. 프로세스 (process)
        if self.top_cpu_processes:
            all_cpu_process_blocks = []
            for proc_data in self.top_cpu_processes:
                current_cpu_process_block_parts = []
                current_cpu_process_block_parts.append(f"  Process: {proc_data.get('Name', 'N/A')} (ID: {proc_data.get('Id', 'N/A')})")
                current_cpu_process_block_parts.append(f"    CPU: {proc_data.get('CPU', 'N/A')}")
                current_cpu_process_block_parts.append(f"    WS (Memory): {proc_data.get('WS', 'N/A')}")
                current_cpu_process_block_parts.append(f"    Path: {proc_data.get('Path', 'N/A')}")
                all_cpu_process_blocks.append('\n'.join(current_cpu_process_block_parts))
            
            formatted_cpu_processes_str = '\n\n'.join(all_cpu_process_blocks)
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}CPU 상위 {len(self.top_cpu_processes)}개 프로세스:{_RESET}\n"
                f"{formatted_cpu_processes_str}"
            )
        if self.top_memory_processes:
            all_memory_process_blocks = []
            for proc_data in self.top_memory_processes:
                current_memory_process_block_parts = []
                current_memory_process_block_parts.append(f"  Process: {proc_data.get('Name', 'N/A')} (ID: {proc_data.get('Id', 'N/A')})")
                current_memory_process_block_parts.append(f"    CPU: {proc_data.get('CPU', 'N/A')}")
                current_memory_process_block_parts.append(f"    WS (Memory): {proc_data.get('WS', 'N/A')}")
                current_memory_process_block_parts.append(f"    Path: {proc_data.get('Path', 'N/A')}")
                all_memory_process_blocks.append('\n'.join(current_memory_process_block_parts))
            
            formatted_memory_processes_str = '\n\n'.join(all_memory_process_blocks)
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}메모리 상위 {len(self.top_memory_processes)}개 프로세스:{_RESET}\n"
                f"{formatted_memory_processes_str}"
            )
        if self.ai_ide_processes_info:
            formatted_ai_processes_str = '\n'.join([f"  {p}" for p in self.ai_ide_processes_info])
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}AI IDE 프로세스:{_RESET}\n"
                f"{formatted_ai_processes_str}"
            )
        if self.tasklist_info:
            formatted_tasklist_str = '\n'.join([f"  {pid}: {name}" for pid, name in self.tasklist_info])
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}작업 목록(Image_Name PID):{_RESET}\n"
                f"{formatted_tasklist_str}"
            )

        # 5. 프로젝트 (project)
        if self.project_info:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}프로젝트 정보:{_RESET}\n"
                f"{self.project_info}"
            )
        if self.python_imports_info:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}Python 임포트 정보:{_RESET}\n"
                f"{self.python_imports_info}"
            )

        # 6. 기타 편의 (convenience)
        if self.lta is not None:
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}QC_MODE (Local Test Activate):{_RESET} {'활성화' if self.lta else '비활성화'}"
            )
        if self.window_titles:
            formatted_titles_str = '\n'.join([f"  {t}" for t in self.window_titles])
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}창 제목:{_RESET}\n"
                f"{formatted_titles_str}"
            )
        if self.stock_info:
            from collections import defaultdict
            
            grouped_stocks = defaultdict(list)
            for item in self.stock_info:
                key = item.code if item.code else item.name
                grouped_stocks[key].append(item)

            all_ticker_blocks = []
            for ticker, items in grouped_stocks.items():
                ticker_block_lines = []
                # 그룹의 첫 번째 항목에서 대표 이름을 가져옵니다.
                stock_name = items[0].name
                
                # 티커(이름) 형식으로 헤더를 추가합니다.
                header = f"  {ticker}({stock_name})"
                ticker_block_lines.append(header)
                
                for item in items:
                    # 각 출처의 정보 라인을 포맷합니다.
                    if item.comparison_score: # 통계 정보는 별도로 처리
                        continue
                    reason_str = f" (N/A 사유: {item.reason})" if item.reason else ""
                    line = f"    {item.price}(현재가)    # {item.source_date} 일자 {item.source}{reason_str}"
                    ticker_block_lines.append(line)
                
                # 통계 정보가 있는 StockInfoItem을 찾아서 출력
                for item in items:
                    if item.comparison_score:
                        score_line = f"    {item.comparison_value}(현재가)    # {item.source_date} 일자 {item.source} ({item.comparison_score})"
                        ticker_block_lines.append(score_line)
                        break # 통계 정보는 티커당 하나만 있다고 가정
                
                all_ticker_blocks.append('\n'.join(ticker_block_lines)) # 각 티커 블록을 리스트에 추가

            formatted_stocks_str = '\n\n'.join(all_ticker_blocks) # 티커 블록 사이에 두 줄 개행
            parts.append(
                f"{PK_UNDERLINE}\n"
                f"{_PK_COLORS['BRIGHT_CYAN']}주식 정보 (# 데이터근거 및 출처):{_RESET}\n"
                f"{formatted_stocks_str}"
            )

        return "\n".join(parts) if parts else "수집된 정보 없음"

    def __repr__(self):
        return self.__str__()

    def _format_connected_drives_info(self, raw_info: str) -> str:
        lines = raw_info.strip().split('\n')
        if not lines:
            return ""

        # Assuming the first line is header, second is separator, rest are data
        # We need to parse the header to get column names and their start/end positions
        # This is a simplified parsing, might need more robust logic for real-world fixed-width data

        # Find header and data lines
        header_line = ""
        data_lines = []

        for line in lines:
            if '---' in line:  # Separator line
                continue
            if not header_line:  # First non-separator line is header
                header_line = line
            else:  # Subsequent non-separator lines are data
                data_lines.append(line)

        if not header_line or not data_lines:
            return raw_info  # Return original if parsing fails

        # Extract column names and their approximate widths/positions
        headers = []
        current_pos = 0
        for i, char in enumerate(header_line):
            if char != ' ' and (i == 0 or header_line[i - 1] == ' '):
                # Start of a new header
                headers.append({'name': char, 'start': i})
            elif char == ' ' and headers and headers[-1]['name'][-1] != ' ':
                # End of a header, update its name
                headers[-1]['name'] += char
            elif char != ' ' and headers:
                headers[-1]['name'] += char

        # Clean up header names
        for h in headers:
            h['name'] = h['name'].strip()

            # Format the output
            all_drive_blocks = []
            for data_line in data_lines:
                if not data_line.strip():
                    continue

                drive_data = {}
                for i in range(len(headers)):
                    start = headers[i]['start']
                    end = headers[i + 1]['start'] if i + 1 < len(headers) else len(data_line)
                    value = data_line[start:end].strip()
                    drive_data[headers[i]['name']] = value

                current_drive_block_parts = []
                if 'Drive' in drive_data and drive_data['Drive']:
                    current_drive_block_parts.append(f"  Drive {drive_data['Drive']}")
                    for key, value in drive_data.items():
                        if key != 'Drive' and value:
                            current_drive_block_parts.append(f"    {key}: {value}")
                elif 'TOTAL' in drive_data and drive_data['TOTAL']:
                    current_drive_block_parts.append(f"  TOTAL:")
                    for key, value in drive_data.items():
                        if key != 'TOTAL' and value:
                            current_drive_block_parts.append(f"    {key}: {value}")

                if current_drive_block_parts:
                    all_drive_blocks.append('\n'.join(current_drive_block_parts))

            return '\n\n'.join(all_drive_blocks)
