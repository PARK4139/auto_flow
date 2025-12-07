"""
FastAPI 기반 대시보드 서버.
PkInterestingInfos와 기온 데이터를 웹 대시보드로 제공합니다.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional
import logging
from datetime import datetime

from pk_internal_tools.pk_functions.get_pk_interesting_infos import get_pk_interesting_infos
from pk_internal_tools.pk_functions.get_temperature_history_from_db import get_temperature_history_from_db
from pk_internal_tools.pk_functions.get_current_temperature_degree_celcious import get_current_temperature_degree_celcious
from pk_internal_tools.pk_functions.get_p110m_energy_aggregated_for_graph import get_p110m_energy_aggregated_for_graph
from pk_internal_tools.pk_functions.get_p110m_energy_history_from_db import get_p110m_energy_history_from_db
from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForEnsureInfoPrinted
import os

app = FastAPI(title="PK System Dashboard", version="1.0.0")

# 정적 파일 서빙 (CSS, JS 등)
static_dir = Path(__file__).parent / "dashboard_static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """대시보드 메인 페이지"""
    html_content = get_dashboard_html()
    return HTMLResponse(content=html_content)


@app.get("/api/interesting-infos")
async def get_interesting_infos():
    """PkInterestingInfos 데이터를 JSON으로 반환"""
    try:
        data = get_pk_interesting_infos(flags=SetupOpsForEnsureInfoPrinted.ALL)
        
        # dataclass를 dict로 변환
        result = {
            "date": data.date,
            "time": data.time,
            "day_of_week": data.day_of_week,
            "location": data.location,
            "weather_infos": data.weather_infos,
            "os_info": data.os_info,
            "screen_info": data.screen_info,
            "connected_drives_info": data.connected_drives_info,
            "wifi_profile_name": data.wifi_profile_name,
            "wifi_password": "***" if data.wifi_password else None,  # 보안
            "window_titles": data.window_titles,
            "processes_info": data.processes_info[:50],  # 최대 50개만
            "tasklist_info": data.tasklist_info[:50],
            "image_names_info": data.image_names_info[:50],
            "ai_ide_processes_info": data.ai_ide_processes_info,
            "top_cpu_processes": data.top_cpu_processes,
            "top_memory_processes": data.top_memory_processes,
            "project_info": data.project_info,
            "python_imports_info": data.python_imports_info,
            "stock_info": [
                {
                    "name": item.name,
                    "code": item.code,
                    "price": item.price,
                    "source": item.source,
                    "source_date": item.source_date
                }
                for item in (data.stock_info or [])
            ]
        }
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"interesting-infos 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/temperature/current")
async def get_current_temperature():
    """현재 기온 조회"""
    try:
        temperature = get_current_temperature_degree_celcious()
        if temperature is None:
            raise HTTPException(status_code=404, detail="기온 데이터를 가져올 수 없습니다")
        return JSONResponse(content={"temperature": temperature, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        logging.error(f"현재 기온 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/temperature/history")
async def get_temperature_history(hours: int = 24, limit: Optional[int] = None):
    """기온 히스토리 조회 (그래프용)"""
    try:
        history = get_temperature_history_from_db(hours=hours, limit=limit)
        result = [
            {
                "temperature": item["temperature"],
                "collected_at": item["collected_at"].isoformat(),
                "city": item["city"]
            }
            for item in history
        ]
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"기온 히스토리 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def get_dashboard_html() -> str:
    """대시보드 HTML 템플릿 반환 (모바일 퍼스트 디자인)"""
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>PK System Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        :root {
            --primary-color: #667eea;
            --primary-dark: #5568d3;
            --secondary-color: #764ba2;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --card-bg: #ffffff;
            --text-primary: #333333;
            --text-secondary: #666666;
            --border-radius: 16px;
            --shadow: 0 4px 20px rgba(0,0,0,0.1);
            --shadow-hover: 0 8px 30px rgba(0,0,0,0.15);
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg-gradient);
            background-attachment: fixed;
            color: var(--text-primary);
            padding: 12px;
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .container {
            max-width: 100%;
            margin: 0 auto;
        }
        
        /* 헤더 - 모바일 최적화 */
        .header {
            background: var(--card-bg);
            padding: 16px;
            border-radius: var(--border-radius);
            margin-bottom: 16px;
            box-shadow: var(--shadow);
            position: sticky;
            top: 12px;
            z-index: 100;
        }
        
        .header h1 {
            color: var(--primary-color);
            margin-bottom: 8px;
            font-size: 24px;
            font-weight: 700;
        }
        
        .header-time {
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }
        
        .refresh-btn {
            width: 100%;
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 14px 20px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            touch-action: manipulation;
        }
        
        .refresh-btn:active {
            background: var(--primary-dark);
            transform: scale(0.98);
        }
        
        /* 기온 카드 - 모바일 퍼스트 */
        .temperature-card {
            background: var(--card-bg);
            padding: 24px;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin-bottom: 16px;
            text-align: center;
        }
        
        .temperature-card h2 {
            color: var(--primary-color);
            margin-bottom: 16px;
            font-size: 18px;
            font-weight: 600;
        }
        
        .temperature-display {
            font-size: 64px;
            font-weight: 700;
            color: var(--primary-color);
            margin: 20px 0;
            line-height: 1;
        }
        
        .temperature-location {
            font-size: 14px;
            color: var(--text-secondary);
            margin-top: 12px;
        }
        
        /* 차트 컨테이너 */
        .chart-container {
            background: var(--card-bg);
            padding: 20px;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin-bottom: 16px;
        }
        
        .chart-container h2 {
            color: var(--primary-color);
            margin-bottom: 16px;
            font-size: 18px;
            font-weight: 600;
        }
        
        #temperature-chart {
            height: 300px;
            width: 100%;
        }
        
        /* 카드 그리드 - 모바일 퍼스트 */
        .card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            margin-bottom: 16px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .card:active {
            transform: scale(0.98);
        }
        
        .card h2 {
            color: var(--primary-color);
            margin-bottom: 16px;
            font-size: 18px;
            font-weight: 600;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 12px;
        }
        
        .info-item {
            margin: 12px 0;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 10px;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .info-label {
            font-weight: 600;
            color: var(--text-primary);
            display: block;
            margin-bottom: 4px;
        }
        
        .info-value {
            color: var(--text-secondary);
        }
        
        .process-list {
            max-height: 250px;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        .process-item {
            padding: 12px;
            margin: 8px 0;
            background: #f8f9fa;
            border-radius: 10px;
            font-size: 13px;
            line-height: 1.5;
        }
        
        .process-item strong {
            color: var(--primary-color);
            display: block;
            margin-bottom: 4px;
        }
        
        .loading {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        /* 스크롤바 스타일링 (모바일) */
        .process-list::-webkit-scrollbar {
            width: 6px;
        }
        
        .process-list::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        .process-list::-webkit-scrollbar-thumb {
            background: var(--primary-color);
            border-radius: 10px;
        }
        
        /* PC 대응 - 태블릿 이상 */
        @media (min-width: 768px) {
            body {
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
            }
            
            .header {
                padding: 24px;
            }
            
            .header h1 {
                font-size: 32px;
            }
            
            .refresh-btn {
                width: auto;
                display: inline-block;
                padding: 12px 24px;
            }
            
            .temperature-display {
                font-size: 80px;
            }
            
            #temperature-chart {
                height: 400px;
            }
            
            .grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }
            
            .card {
                margin-bottom: 0;
            }
            
            .card:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-hover);
            }
        }
        
        /* PC 대응 - 데스크톱 */
        @media (min-width: 1024px) {
            .grid {
                grid-template-columns: repeat(3, 1fr);
            }
            
            .temperature-card {
                padding: 32px;
            }
            
            .chart-container {
                padding: 24px;
            }
        }
        
        /* 큰 화면 대응 */
        @media (min-width: 1400px) {
            .container {
                max-width: 1400px;
            }
            
            .grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }
        
        /* 다크모드 지원 (선택사항) */
        @media (prefers-color-scheme: dark) {
            :root {
                --card-bg: #1a1a1a;
                --text-primary: #ffffff;
                --text-secondary: #b0b0b0;
            }
            
            .info-item, .process-item {
                background: #2a2a2a;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌡️ PK System Dashboard</h1>
            <div class="header-time" id="current-time"></div>
            <button class="refresh-btn" onclick="loadAllData()">🔄 새로고침</button>
        </div>
        
        <!-- 기온 섹션 -->
        <div class="temperature-card">
            <h2>🌡️ 현재 기온</h2>
            <div class="temperature-display" id="current-temperature">로딩 중...</div>
            <div class="temperature-location">
                <span class="info-label">위치:</span>
                <span id="location">-</span>
            </div>
        </div>
        
        <!-- 기온 그래프 -->
        <div class="chart-container">
            <h2>📈 기온 추이 (최근 24시간)</h2>
            <div id="temperature-chart"></div>
        </div>
        
        <!-- P110M 에너지 그래프 -->
        <div class="chart-container">
            <h2>⚡ P110M 에너지 사용량 (년간)</h2>
            <div style="margin-bottom: 12px;">
                <select id="energy-period" onchange="loadP110mEnergyData()" style="padding: 8px; border-radius: 8px; border: 1px solid #ddd; font-size: 14px;">
                    <option value="year">1년</option>
                    <option value="month">1개월</option>
                    <option value="week">1주일</option>
                    <option value="day">1일</option>
                </select>
            </div>
            <div id="energy-chart"></div>
        </div>
        
        <!-- 정보 그리드 -->
        <div class="grid">
            <div class="card">
                <h2>📅 날짜/시간</h2>
                <div class="info-item">
                    <span class="info-label">날짜</span>
                    <span class="info-value" id="date">-</span>
                </div>
                <div class="info-item">
                    <span class="info-label">시간</span>
                    <span class="info-value" id="time">-</span>
                </div>
                <div class="info-item">
                    <span class="info-label">요일</span>
                    <span class="info-value" id="day-of-week">-</span>
                </div>
            </div>
            
            <div class="card">
                <h2>🌤️ 날씨 정보</h2>
                <div id="weather-info">로딩 중...</div>
            </div>
            
            <div class="card">
                <h2>💻 시스템 정보</h2>
                <div class="info-item">
                    <span class="info-label">OS</span>
                    <span class="info-value" id="os-info">-</span>
                </div>
                <div class="info-item">
                    <span class="info-label">화면</span>
                    <span class="info-value" id="screen-info">-</span>
                </div>
            </div>
            
            <div class="card">
                <h2>📊 CPU 상위 프로세스</h2>
                <div class="process-list" id="top-cpu-processes">로딩 중...</div>
            </div>
            
            <div class="card">
                <h2>💾 메모리 상위 프로세스</h2>
                <div class="process-list" id="top-memory-processes">로딩 중...</div>
            </div>
            
            <div class="card">
                <h2>📈 주식 정보</h2>
                <div id="stock-info">로딩 중...</div>
            </div>
        </div>
    </div>
    
    <script>
        // 시간 표시 업데이트
        function updateCurrentTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = 
                now.toLocaleString('ko-KR', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric',
                    hour: '2-digit', 
                    minute: '2-digit',
                    second: '2-digit'
                });
        }
        setInterval(updateCurrentTime, 1000);
        updateCurrentTime();
        
        // 현재 기온 로드
        async function loadCurrentTemperature() {
            try {
                const response = await fetch('/api/temperature/current');
                const data = await response.json();
                document.getElementById('current-temperature').textContent = 
                    data.temperature ? `${data.temperature.toFixed(1)}°C` : 'N/A';
            } catch (error) {
                console.error('기온 로드 실패:', error);
                document.getElementById('current-temperature').textContent = '오류';
            }
        }
        
        // 기온 히스토리 로드 및 그래프 그리기
        async function loadTemperatureHistory() {
            try {
                const response = await fetch('/api/temperature/history?hours=24');
                const data = await response.json();
                
                if (data.length === 0) {
                    document.getElementById('temperature-chart').innerHTML = 
                        '<div class="loading">데이터가 없습니다.</div>';
                    return;
                }
                
                // 시간순 정렬 (오래된 것부터)
                const sortedData = data.sort((a, b) => 
                    new Date(a.collected_at) - new Date(b.collected_at)
                );
                
                const times = sortedData.map(d => new Date(d.collected_at));
                const temps = sortedData.map(d => d.temperature);
                
                const trace = {
                    x: times,
                    y: temps,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: '기온',
                    line: { color: '#667eea', width: 2 },
                    marker: { size: 6 }
                };
                
                const layout = {
                    title: '기온 추이',
                    xaxis: { title: '시간' },
                    yaxis: { title: '기온 (°C)' },
                    responsive: true,
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)'
                };
                
                Plotly.newPlot('temperature-chart', [trace], layout, {responsive: true});
            } catch (error) {
                console.error('기온 히스토리 로드 실패:', error);
                document.getElementById('temperature-chart').innerHTML = 
                    '<div class="loading">그래프를 불러올 수 없습니다.</div>';
            }
        }
        
        // Interesting Infos 로드
        async function loadInterestingInfos() {
            try {
                const response = await fetch('/api/interesting-infos');
                const data = await response.json();
                
                // 기본 정보
                document.getElementById('date').textContent = data.date || '-';
                document.getElementById('time').textContent = data.time || '-';
                document.getElementById('day-of-week').textContent = data.day_of_week || '-';
                document.getElementById('location').textContent = data.location || '-';
                document.getElementById('os-info').textContent = data.os_info || '-';
                document.getElementById('screen-info').textContent = data.screen_info || '-';
                
                // 날씨 정보
                const weatherDiv = document.getElementById('weather-info');
                if (data.weather_infos && data.weather_infos.length > 0) {
                    weatherDiv.innerHTML = data.weather_infos.map(info => 
                        `<div class="info-item"><span class="info-value">${info}</span></div>`
                    ).join('');
                } else {
                    weatherDiv.innerHTML = '<div class="info-item"><span class="info-value">날씨 정보 없음</span></div>';
                }
                
                // CPU 프로세스
                const cpuDiv = document.getElementById('top-cpu-processes');
                if (data.top_cpu_processes && data.top_cpu_processes.length > 0) {
                    cpuDiv.innerHTML = data.top_cpu_processes.slice(0, 10).map(proc => 
                        `<div class="process-item">
                            <strong>${proc.Name || 'N/A'}</strong><br>
                            CPU: ${proc.CPU || 'N/A'}% | 메모리: ${proc.WS || 'N/A'}
                        </div>`
                    ).join('');
                } else {
                    cpuDiv.textContent = '데이터 없음';
                }
                
                // 메모리 프로세스
                const memDiv = document.getElementById('top-memory-processes');
                if (data.top_memory_processes && data.top_memory_processes.length > 0) {
                    memDiv.innerHTML = data.top_memory_processes.slice(0, 10).map(proc => 
                        `<div class="process-item">
                            <strong>${proc.Name || 'N/A'}</strong><br>
                            CPU: ${proc.CPU || 'N/A'}% | 메모리: ${proc.WS || 'N/A'}
                        </div>`
                    ).join('');
                } else {
                    memDiv.textContent = '데이터 없음';
                }
                
                // 주식 정보
                const stockDiv = document.getElementById('stock-info');
                if (data.stock_info && data.stock_info.length > 0) {
                    stockDiv.innerHTML = data.stock_info.map(stock => 
                        `<div class="info-item">
                            <span class="info-label">${stock.name}</span>
                            <span class="info-value">${stock.code || 'N/A'}<br>가격: ${stock.price}<br>출처: ${stock.source}</span>
                        </div>`
                    ).join('');
                } else {
                    stockDiv.innerHTML = '<div class="info-item"><span class="info-value">주식 정보 없음</span></div>';
                }
                
            } catch (error) {
                console.error('정보 로드 실패:', error);
            }
        }
        
        // 모든 데이터 로드
        async function loadAllData() {
            await Promise.all([
                loadCurrentTemperature(),
                loadTemperatureHistory(),
                loadInterestingInfos()
            ]);
        }
        
        // 초기 로드
        loadAllData();
        
        // 30초마다 자동 새로고침
        setInterval(loadAllData, 30000);
    </script>
</body>
</html>
    """

