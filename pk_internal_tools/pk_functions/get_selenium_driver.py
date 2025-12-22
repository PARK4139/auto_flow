from pk_internal_tools.pk_functions.get_webdriver_options_customed import get_webdriver_options_customed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_selenium_driver(headless_mode):
    from pk_internal_tools.pk_functions.get_webdriver_options_customed import get_webdriver_options_customed
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    import selenium.webdriver as webdriver

    options = get_webdriver_options_customed(browser_debug_mode=headless_mode)

    # 드라이버 as 크롬브라우저
    driver = webdriver.Chrome(options=options)
    # service = Service('path/to/chromedriver')  # 크롬 드라이버 경로
    # driver = webdriver.Chrome(service=service, options=options)

    # 브라우저 exec
    driver.get('about:blank')
    # driver.get('http://www.naver.com')

    # driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")  # hide plugin 0EA
    # driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")  # hide own lanuages
    # driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")  # hide own gpu # WebGL렌더러를 Nvidia회사와 GTX980Ti엔진인 ‘척’ 하는 방법입니다.

    # 플러그인 언어 소유GPU 숨기기
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}});")
    # driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}});")
    driver.execute_script(
        "const getParameter = WebGLRenderingContext.getParameter; WebGLRenderingContext.prototype.getParameter = function(parameter) { if (parameter === 37445) { return 'NVIDIA Corporation'; } if (parameter === 37446) { return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine'; } return getParameter(parameter); };")
    return driver


@ensure_seconds_measured
def get_selenium_driver_fallback(browser_debug_mode, proxy=None):
    import inspect
    import selenium.webdriver as webdriver
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # 드라이버 옵션
    # options=get_webdriver_options_customed(browser_show=browser_debug_mode)
    options = get_webdriver_options_customed(browser_debug_mode=browser_debug_mode, proxy=proxy)

    # 드라이버 as 크롬브라우저
    # service=Service('path/to/chromedriver')  # 크롬 드라이버 경로
    # driver=webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options)

    # 브라우저 exec
    driver.get('about:blank')
    # driver.get('http://www.naver.com')

    # cookies (가짜)
    # cookies=[
    #     {"name": "cf_clearance", "value": "쿠키값", "domain": "yadongplay1.net"},
    # ]
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    # 플러그인 언어 소유GPU 숨기기
    # driver.execute_script(        "const getParameter=WebGLRenderingContext.getParameter; WebGLRenderingContext.prototype.getParameter=function(parameter) { if (parameter === 37445) { return 'NVIDIA Corporation'; } if (parameter === 37446) { return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine'; } return getParameter(parameter); };")
    # driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}});")# hide plugin 0EA
    # driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}});")  # hide own lanuages
    # driver.execute_script("const getParameter=WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter=function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")  # hide own gpu # WebGL렌더러를 Nvidia회사와 GTX980Ti엔진인 ‘척’ 하는 방법입니다.

    return driver
