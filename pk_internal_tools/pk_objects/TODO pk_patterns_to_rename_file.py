pattern=r'(\[.*?\])'  # [문자열]
pattern=r'\d{4}_\d{2}_\d{2}_(월|화|수|목|금|토|일)_\d{2}_\d{2}_\d{2}_\d{3}',
pattern=r'\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}',
pattern=r'_\d{11}_\d{11}_',
pattern=r'_\d{10}_\d{10}_',
pattern=r'_\d{11}_',
pattern=r'\d{4}_\d{2}_\d{2}_(월|화|수|목|금|토|일)_\d{2}_\d{2}_\d{2}_\d{3}',
pattern=r'jhp##\d{4}_\d{2}_\d{2}', text_new="[jhp##]",
pattern=r'jhp##\d{8}', text_new="[jhp##]",
pattern=r'\$\d{22}', text_new="_",
pattern=r'_\d{29}_', text_new="_",
pattern=r'\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}', text_new=".",
pattern=r'_\d{8}_', text_new=".",
pattern=r'_\d{11}.', text_new=".",
pattern=r'_\d{11}_', text_new=".",
pattern=r'_\d{11}', text_new="",
pattern=r'^seg ', text_new="_",
pattern=r'^_', text_new="[시작문자]",
pattern=r'^#', text_new="[시작문자]",
pattern=r'^The ', text_new="[시작문자]",
pattern=r'_$', text_new="[끝문자]",
pattern=r'\(([^)]+)\)(?=.*\(\1\))', text_new="[중복문자]",
pattern=r'^.', text_new="_"  # 시작문자 # 첫글자가 없어진다... 씆지말자
pattern=r'^ ', text_new="_"  # 시작문자 # 업데이트가 되긴하는데 ^_ 이 왜 안되는지 모르겠다.
pattern=r'_\d{11}$', text_new="" # 끝문자 # 끝문자 안되는 것 같은데...
pattern=r'_\d+$', text_new="" # 끝문자
pattern=r'_\d{10}_\d{10}_', text_new=""
pattern=r'_\d{10}_', text_new=""
pattern= r'\d{10}', text_new=""
pattern=r'\$\d{22}', text_new=""
pattern=r'_\d{11}', text_new=""