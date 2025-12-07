def test_example_call_pythonfile_as_new_window():
    # not recommanded way
    python_file_base = d_pk_system
    python_filename = rf"pk_push_project_to_github.py"
    python_file = Path(rf'{python_file_base}/{python_filename}')
    python_calling_program = 'start "" python'
    os.chdir(python_file_base)
    ensure_command_executed(cmd=f'{python_calling_program} "{python_file}"')


