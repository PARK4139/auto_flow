import subprocess
import logging
import re
import csv
import io

def get_top_processes_info() -> dict:
    """
    PowerShell을 사용하여 CPU 및 메모리 사용량 상위 10개 프로세스 정보를 가져옵니다.
    """
    top_processes = {
        'top_cpu': [],
        'top_memory': []
    }

    # CPU 상위 10개 프로세스
    cpu_command = """
    Get-Process | Sort-Object CPU -Desc |
    Select-Object -First 10 Name, Id, CPU, WS, Path | ConvertTo-Csv -NoTypeInformation
    """
    # 메모리(Working Set) 상위 10개 프로세스
    memory_command = """
    Get-Process | Sort-Object WS -Desc |
    Select-Object -First 10 Name, Id, CPU, WS, Path | ConvertTo-Csv -NoTypeInformation
    """

    for category, command in [('top_cpu', cpu_command), ('top_memory', memory_command)]:
        try:
            # PowerShell 명령 실행
            process = subprocess.run(
                ["powershell.exe", "-Command", command],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            output = process.stdout.strip()

            # CSV 파싱을 위해 csv 모듈 사용
            csv_reader = csv.reader(io.StringIO(output))
            
            try:
                headers = next(csv_reader)
            except StopIteration:
                # 출력이 비어있는 경우
                logging.warning(f"PowerShell에서 {category}에 대한 출력이 없습니다.")
                continue

            for values in csv_reader:
                if not values:
                    continue
                
                proc_data = dict(zip(headers, values))
                
                # Convert numeric values
                for key in ['Id', 'CPU', 'WS']:
                    if key in proc_data and proc_data[key]:
                        try:
                            # PowerShell에서 오는 CPU 값은 현재 문화권에 따라 소수점 기호가 다를 수 있음 (예: 쉼표)
                            # 이를 점으로 통일하여 변환 오류 방지
                            value_str = proc_data[key].replace(',', '.')
                            if key == 'CPU':
                                proc_data[key] = round(float(value_str), 2)
                            else:
                                proc_data[key] = int(float(value_str))
                        except (ValueError, TypeError):
                            pass # Keep as string if conversion fails

                top_processes[category].append(proc_data)

        except subprocess.CalledProcessError as e:
            logging.error(f"PowerShell 명령 실행 중 오류 ({category}): {e}")
            logging.error(f"Stdout: {e.stdout}")
            logging.error(f"Stderr: {e.stderr}")
        except Exception as e:
            logging.error(f"프로세스 정보 파싱 중 오류 ({category}): {e}")

    return top_processes

if __name__ == '__main__':
    # Example usage for testing
    logging.basicConfig(level=logging.DEBUG)
    result = get_top_processes_info()
    logging.debug(f"Top CPU Processes: {result['top_cpu']}")
    logging.debug(f"Top Memory Processes: {result['top_memory']}")
