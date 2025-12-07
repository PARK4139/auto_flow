#!/usr/bin/env python3
"""
WSL/Linux 환경에서 GitHub용 SSH 키 자동 설정 스크립트
- SSH 키 생성
- ssh-agent 실행 및 ssh-add 등록
- 공개 키 출력
- Git 리모트 SSH URL로 전환
- 자동 등록(PAT 필요) 또는 수동 등록 선택 가능
"""

import os
import subprocess
import sys
import requests

def run_cmd(cmd, check=True):
    print(f"\n[실행 중] {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def ensure_ssh_key_generated(email):
    ssh_dir = os.path.expanduser("~/.ssh")
    key_path = os.path.join(ssh_dir, "id_rsa")
    if not os.path.exists(key_path):
        print(f" SSH 키가 없습니다. 새로 생성합니다 (이메일: {email})")
        os.makedirs(ssh_dir, exist_ok=True)
        run_cmd(f'ssh-keygen -t rsa -b 4096 -C "{email}" -f "{key_path}" -N ""')
    else:
        print(" 이미 SSH 키가 존재합니다. 생성 생략.")

def ensure_ssh_agent_started_and_key_added():
    print(" ssh-agent 실행 및 SSH 키 등록")
    script = '''
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa
    '''
    run_cmd(f'bash -c \'{script}\'')

def show_public_key():
    pubkey_path = os.path.expanduser("~/.ssh/id_rsa.pub")
    if not os.path.exists(pubkey_path):
        print(" 공개 키가 존재하지 않습니다.")
        return None
    print(" 아래 공개 키를 복사해 GitHub에 등록하세요:\n")
    with open(pubkey_path, "r") as f:
        key = f.read().strip()
        print(key)
        return key

def open_github_ssh_key_page():
    print(" GitHub SSH 키 등록 페이지를 브라우저로 엽니다.")
    run_cmd("xdg-open https://github.com/settings/keys || powershell.exe start https://github.com/settings/keys")

def upload_ssh_key_to_github(pubkey, github_token, key_title):
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "title": key_title,
        "key": pubkey
    }

    response = requests.post("https://api.github.com/user/keys", headers=headers, json=data)

    if response.status_code == 201:
        print(" SSH 키가 GitHub에 성공적으로 등록되었습니다.")
        return True
    else:
        print(f" 등록 실패: {response.status_code} - {response.text}")
        return False

def ensure_github_url_converted_to_ssh():
    print(" Git 리모트 URL을 SSH 형식으로 전환합니다.")
    try:
        origin_url = subprocess.check_output("git remote get-url origin", shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        print("️ 현재 디렉토리는 Git 리포지토리가 아닙니다. 스킵합니다.")
        return

    if origin_url.startswith("git@"):
        print(" 이미 SSH 형식입니다:", origin_url)
    elif "github.com" in origin_url:
        repo_path = origin_url.split("github.com/")[-1]
        ssh_url = f"git@github.com:{repo_path}"
        run_cmd(f"git remote set-url origin {ssh_url}")
        print(f" 리모트 URL을 SSH 형식으로 변경함: {ssh_url}")
    else:
        print("️ GitHub 리포지토리가 아닌 것 같습니다. 수동 설정 권장.")

def main():
    print(" GitHub용 SSH 키 자동 설정 스크립트 시작")
    email = input(" GitHub에 등록된 이메일 주소를 입력하세요: ").strip()
    if not email:
        print(" 이메일이 입력되지 않았습니다.")
        sys.exit(1)

    ensure_ssh_key_generated(email)
    ensure_ssh_agent_started_and_key_added()
    public_key = show_public_key()
    if not public_key:
        sys.exit(1)

    # 모드 선택
    choice = input("\n 공개 키를 GitHub에 어떻게 등록할까요?\n1.  자동 등록 (PAT 필요)\n2.  수동 등록 (브라우저 열기)\n선택 (1/2): ").strip()

    success = False
    if choice == "1":
        github_token = input(" GitHub Personal Access Token (PAT)을 입력하세요: ").strip()
        if not github_token.startswith("ghp_") and not github_token.startswith("github_pat_"):
            print(" 유효하지 않은 토큰 형식입니다.")
            sys.exit(1)
        success = upload_ssh_key_to_github(
            pubkey=public_key,
            github_token=github_token,
            key_title="WSL pk_system 자동화 환경"
        )
    else:
        open_github_ssh_key_page()

    ensure_github_url_converted_to_ssh()

    if success:
        print(" 완료! GitHub에서 SSH 키가 정상 등록되었는지 확인하세요: https://github.com/settings/keys")
    else:
        print("️ SSH 키 등록에 실패했거나 수동 등록을 선택했습니다. GitHub 설정 페이지에서 직접 확인하세요: https://github.com/settings/keys")

if __name__ == "__main__":
    main()
