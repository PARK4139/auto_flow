from pathlib import Path

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_pk_root() -> Path | None:
    """
        TODO: Write docstring for get_pk_root.
    """
    try:

        """
        return: 프로젝트 루트 (pyproject.toml이 있는 곳)
        """

        # pyproject.toml이 있는 프로젝트 루트를 우선적으로 찾음
        current = Path.cwd().resolve()
        max_depth = 10  # 최대 10단계 상위 디렉토리까지 검색
        depth = 0

        pk_candidates = []

        while depth < max_depth:
            # pyproject.toml이 있는지 먼저 확인 (프로젝트 루트 우선)
            pyproject_toml = current / 'pyproject.toml'
            if pyproject_toml.exists():
                try:
                    import toml
                    config = toml.load(pyproject_toml)
                    if config.get('project', {}).get('name') == 'pk_system':
                        # 프로젝트 루트를 반환 (pk_system가 아닌 실제 루트)
                        # pyproject.toml이 있는 디렉토리가 프로젝트 루트

                        return current
                except Exception as e:
                    pass

            # 상위 디렉토리로 이동
            parent = current.parent
            if parent == current:  # 루트 디렉토리에 도달
                break
            current = parent
            depth += 1

        # pyproject.toml을 찾지 못한 경우, pk_internal_tools 디렉토리로 찾기 (하위 호환성)
        current = Path.cwd().resolve()
        depth = 0
        while depth < max_depth:
            pk_candidate = current / 'pk_internal_tools'
            if pk_candidate.exists() and pk_candidate.is_dir():
                # pk_internal_tools의 부모가 프로젝트 루트일 가능성이 높음
                # 하지만 pk_system/pk_internal_tools인 경우도 있으므로 확인 필요
                # pk_system/pk_internal_tools인 경우, 프로젝트 루트는 pk_system의 부모
                if (current / 'pk_system' / 'pk_internal_tools').exists():
                    # pk_system/pk_internal_tools 구조인 경우

                    return current  # pk_system가 프로젝트 루트가 아님, 상위로
                else:
                    # 일반적인 pk_internal_tools 구조인 경우
                    pk_candidates.append(current)

            parent = current.parent
            if parent == current:
                break
            current = parent
            depth += 1

        # 가장 가까운 pk_system 반환 (현재 작업 디렉토리에 가장 가까운 것)
        if pk_candidates:
            return pk_candidates[0]

        # 3. __file__ 기반 경로 (하위 호환성)
        file_based_path = Path(__file__).resolve().parent.parent.parent.parent.parent

        try:
            import toml
        except ImportError:
            toml = None  # toml 모듈이 없으면 None으로 설정

        if toml and (file_based_path / 'pyproject.toml').exists():
            try:
                config = toml.load(file_based_path / 'pyproject.toml')
                if config.get('project', {}).get('name') == 'pk_system':
                    return file_based_path
            except Exception as e:
                pass

        # 레거시 pk_internal_tools 구조를 위한 추가 확인
        # 만약 현재 프로젝트가 'pk_system/pk_system' 구조가 아니라
        # 'pk_system' 바로 아래에 'pk_internal_tools'가 있는 경우를 처리
        legacy_pk_internal_tools_path = Path(__file__).resolve().parent.parent.parent.parent  # pk_system/src
        if (legacy_pk_internal_tools_path / 'pk_internal_tools').exists() and (legacy_pk_internal_tools_path / 'pk_system').exists():
            # D_PK_ROOT = get_pk_root() 로직에서 D_PK_ROOT = D_PK_ROOT / "src" / "pk_system" 부분이 있으므로
            # 이 경우에는 루트를 'C:\Users\wjdgn\Downloads\pk_system'으로 반환해야 한다.

            return legacy_pk_internal_tools_path.parent

        if (file_based_path / 'pk_internal_tools').exists():
            return file_based_path
        return file_based_path
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
