

if __name__ == '__main__':
    try:
        #  import ensure_pk_project_docker_ran, pk_deprecated_get_d_current_n_like_human, get_f_current_n, get_selenium_driver
        #
        #, d_pk_system

        f_dockerfile_script_list = [
            f'# FROM python:3.12.8-alpine',
            f'# FROM python:3.12-slim # Ubuntu-slim [fail]',
            f'FROM ubuntu:24.04',
            f'WORKDIR /container_workspace',
            f'ENV TZ=Asia/Seoul',
            f'RUN export LANG=en_US.UTF-8',
            f'RUN apt-get update && apt-get install -y \
                        python3 \
                        python3-pip \
                        python3-venv \
                        bash \
                        bash-completion \
                        curl \
                        wget \
                        unzip \
                        nano \
                        ca-certificates \
                        software-properties-common \
                        locales \
                        tzdata \
                        build-essential \
                        pkg-config \
                        libmariadb-dev \
                        gcc \
                        portaudio19-dev \
                        && rm -rf /var/lib/apt/lists/*  # 설치 후 패키지 목록 삭제하여 용량 최적화',
            f'',
            f'RUN python3 -m venv /container_workspace/.venv',
            f'RUN /container_workspace/.venv/bin/pip install --upgrade pip setuptools wheel ',
            f'',
            f'COPY requirements.txt .',
            f'# RUN apt-get install uvicorn',
            f'RUN /container_workspace/.venv/bin/pip install --no-cache-dir -r requirements.txt',
            f'',
            f'COPY . .',
            f'',
            f'CMD ["/container_workspace/.venv/bin/python", "-m", "uvicorn", "project_fastapi.test_project_fastapi:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]',
            f'',
        ]
        # ensure_pk_project_docker_ran(f=rf'{d_pk_system}/project_fastapi.Dockerfile',f_dockerfile_script_list=f_dockerfile_script_list)
        ensure_pk_project_docker_ran(f=rf'{d_pk_system}/test.Dockerfile', dockerfile_script_list=f_dockerfile_script_list)

    except Exception as e:
        # red
        import traceback
        from pk_internal_tools.pk_objects.pk_texts import PkTexts
        logging.debug(f'{PK_UNDERLINE}{PkTexts.EXCEPTION_OCCURRED_S}\n\n')
        logging.debug(f'{traceback.format_exc()}\n')
        logging.debug(f'{PK_UNDERLINE}{PkTexts.EXCEPTION_OCCURRED_E}\n\n')

        # yellow
        f_current= get_f_current_n()
        d_current=pk_deprecated_get_d_current_n_like_human()
        logging.debug(f'{PK_UNDERLINE}{PkTexts.DEBUGGING_NOTE_S}\n')
        logging.debug(f'f_current={f_current}\nd_current={d_current}\n')
        logging.debug(f'{PK_UNDERLINE}{PkTexts.DEBUGGING_NOTE_E}\n')
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_system)
        logging.debug(script_to_run_python_program_in_venv)
