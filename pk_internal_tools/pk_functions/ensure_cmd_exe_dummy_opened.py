

def ensure_cmd_exe_dummy_opened():
	import os

	from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

	for i in enumerate([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]):
		os.system("start "" cmd.exe /t")
		ensure_slept(milliseconds=250)