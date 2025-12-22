"""
FastAPI based dashboard server, now integrated as a router into pk_web_server.
Provides PkInterestingInfos and temperature data to a web dashboard.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime, date, timedelta
from collections import defaultdict

# Lazy imports to avoid circular dependencies and speed up startup
def get_pk_interesting_infos(*args, **kwargs):
    from pk_internal_tools.pk_functions.get_pk_interesting_infos import get_pk_interesting_infos as func
    return func(*args, **kwargs)

def get_temperature_history_from_db(*args, **kwargs):
    from pk_internal_tools.pk_functions.get_temperature_history_from_db import get_temperature_history_from_db as func
    return func(*args, **kwargs)

def get_current_temperature_degree_celcious(*args, **kwargs):
    from pk_internal_tools.pk_functions.get_current_temperature_degree_celcious import get_current_temperature_degree_celcious as func
    return func(*args, **kwargs)

def get_p110m_energy_aggregated_for_graph(*args, **kwargs):
    from pk_internal_tools.pk_functions.get_p110m_energy_aggregated_for_graph import get_p110m_energy_aggregated_for_graph as func
    return func(*args, **kwargs)

def get_p110m_energy_history_from_db(*args, **kwargs):
    from pk_internal_tools.pk_functions.get_p110m_energy_history_from_db import get_p110m_energy_history_from_db as func
    return func(*args, **kwargs)

# Import MemoService and Memo model from memos router
from .memos import MemoService, Memo


import os

router = APIRouter()

# Static files for the dashboard (if any, currently all inline)
# static_dir = Path(__file__).parent.parent / "dashboard_static"
# if static_dir.exists():
#     router.mount("/static", StaticFiles(directory=str(static_dir)), name="static_dashboard")


@router.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """Dashboard main page"""
    html_content = get_dashboard_html()
    return HTMLResponse(content=html_content)


@router.get("/api/memos/stats", summary="메모 통계 조회", tags=["Dashboard"])
async def get_memo_stats(memo_service: MemoService = Depends()):
    """
    메모 관련 통계 데이터를 반환합니다.
    - 총 메모 수
    - 일별 생성된 메모 수
    """
    logging.info("Dashboard API: 메모 통계 조회 요청이 들어왔습니다.")
    try:
        all_memos = memo_service.get_all_memos()
        total_memos = len(all_memos)

        memos_per_day = defaultdict(int)
        for memo in all_memos:
            memo_date = memo.created_at.date()
            memos_per_day[memo_date] += 1
        
        # 날짜 순으로 정렬
        sorted_memos_per_day = sorted([
            {"date": str(d), "count": c} for d, c in memos_per_day.items()
        ], key=lambda x: x["date"])

        result = {
            "total_memos": total_memos,
            "memos_per_day": sorted_memos_per_day
        }
        logging.info(f"Dashboard API: 메모 통계 조회 완료. 총 메모 수: {total_memos}")
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"Failed to get memo stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/interesting-infos")
async def get_interesting_infos():
    """Return PkInterestingInfos data as JSON"""
    try:
        data = get_pk_interesting_infos(flags="ALL")
        
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
            "wifi_password": "***" if data.wifi_password else None,
            "window_titles": data.window_titles,
            "processes_info": data.processes_info[:50],
            "tasklist_info": data.tasklist_info[:50],
            "image_names_info": data.image_names_info[:50],
            "ai_ide_processes_info": data.ai_ide_processes_info,
            "top_cpu_processes": data.top_cpu_processes,
            "top_memory_processes": data.top_memory_processes,
            "project_info": data.project_info,
            "python_imports_info": data.python_imports_info,
            "stock_info": [
                {
                    "name": item.get("name"),
                    "code": item.get("code"),
                    "price": item.get("price"),
                    "source": item.get("source"),
                    "source_date": item.get("source_date")
                }
                for item in (data.stock_info or [])
            ]
        }
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"Failed to get interesting-infos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/temperature/current")
async def get_current_temperature():
    """Get current temperature"""
    try:
        temperature = get_current_temperature_degree_celcious()
        if temperature is None:
            raise HTTPException(status_code=404, detail="Could not retrieve temperature data.")
        return JSONResponse(content={"temperature": temperature, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        logging.error(f"Failed to get current temperature: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/temperature/history")
async def get_temperature_history(hours: int = 24, limit: Optional[int] = None):
    """Get temperature history for graph"""
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
        logging.error(f"Failed to get temperature history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


def get_dashboard_html() -> str:
    """Returns the dashboard HTML template (mobile-first design)"""
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
        
        /* Header - Mobile optimized */
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
        
        /* Temperature Card - Mobile first */
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
        
        /* Chart Container */
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
        
        /* Card Grid - Mobile first */
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
        
        /* Scrollbar styling (mobile) */
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
        
        /* PC - Tablet and above */
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
        
        /* PC - Desktop */
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
        
        /* Large screen */
        @media (min-width: 1400px) {
            .container {
                max-width: 1400px;
            }
            
            .grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }
        
        /* Dark mode support (optional) */
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
        
        <!-- Memo Stats -->
        <div class="chart-container">
            <h2>📝 메모 통계 (일별 생성)</h2>
            <div id="memo-chart"></div>
        </div>

        <!-- Temperature Section -->
        <div class="temperature-card">
            <h2>🌡️ 현재 기온</h2>
            <div class="temperature-display" id="current-temperature">로딩 중...</div>
            <div class="temperature-location">
                <span class="info-label">위치:</span>
                <span id="location">-</span>
            </div>
        </div>
        
        <!-- Temperature Graph -->
        <div class="chart-container">
            <h2>📈 기온 추이 (최근 24시간)</h2>
            <div id="temperature-chart"></div>
        </div>
        
        <!-- P110M Energy Graph -->
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
        
        <!-- Info Grid -->
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
        // Load Memo Stats
        async function loadMemoStats() {
            try {
                const response = await fetch('./api/memos/stats');
                const data = await response.json();

                // Memo Chart
                const dates = data.memos_per_day.map(item => item.date);
                const counts = data.memos_per_day.map(item => item.count);

                const trace = {
                    x: dates,
                    y: counts,
                    type: 'bar',
                    name: '메모 수',
                    marker: { color: '#667eea' }
                };

                const layout = {
                    title: '일별 생성 메모 수',
                    xaxis: { title: '날짜' },
                    yaxis: { title: '메모 수' },
                    responsive: true,
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)'
                };

                Plotly.newPlot('memo-chart', [trace], layout, {responsive: true});

            } catch (error) {
                console.error('Failed to load memo stats:', error);
                document.getElementById('memo-chart').innerHTML =
                    '<div class="loading">Could not load memo stats.</div>';
            }
        }

        // Update current time display
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
        
        // Load current temperature
        async function loadCurrentTemperature() {
            try {
                const response = await fetch('./api/temperature/current');
                const data = await response.json();
                document.getElementById('current-temperature').textContent = 
                    data.temperature ? `${data.temperature.toFixed(1)}°C` : 'N/A';
            } catch (error) {
                console.error('Failed to load temperature:', error);
                document.getElementById('current-temperature').textContent = 'Error';
            }
        }
        
        // Load temperature history and draw graph
        async function loadTemperatureHistory() {
            try {
                const response = await fetch('./api/temperature/history?hours=24');
                const data = await response.json();
                
                if (data.length === 0) {
                    document.getElementById('temperature-chart').innerHTML = 
                        '<div class="loading">No data available.</div>';
                    return;
                }
                
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
                    name: 'Temperature',
                    line: { color: '#667eea', width: 2 },
                    marker: { size: 6 }
                };
                
                const layout = {
                    title: 'Temperature Trend',
                    xaxis: { title: 'Time' },
                    yaxis: { title: 'Temperature (°C)' },
                    responsive: true,
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)'
                };
                
                Plotly.newPlot('temperature-chart', [trace], layout, {responsive: true});
            } catch (error) {
                console.error('Failed to load temperature history:', error);
                document.getElementById('temperature-chart').innerHTML = 
                    '<div class="loading">Could not load graph.</div>';
            }
        }
        
        // Load Interesting Infos
        async function loadInterestingInfos() {
            try {
                const response = await fetch('./api/interesting-infos');
                const data = await response.json();
                
                document.getElementById('date').textContent = data.date || '-';
                document.getElementById('time').textContent = data.time || '-';
                document.getElementById('day-of-week').textContent = data.day_of_week || '-';
                document.getElementById('location').textContent = data.location || '-';
                document.getElementById('os-info').textContent = data.os_info || '-';
                document.getElementById('screen-info').textContent = data.screen_info || '-';
                
                const weatherDiv = document.getElementById('weather-info');
                if (data.weather_infos && data.weather_infos.length > 0) {
                    weatherDiv.innerHTML = data.weather_infos.map(info => 
                        `<div class="info-item"><span class="info-value">${info}</span></div>`
                    ).join('');
                } else {
                    weatherDiv.innerHTML = '<div class="info-item"><span class="info-value">No weather info</span></div>';
                }
                
                const cpuDiv = document.getElementById('top-cpu-processes');
                if (data.top_cpu_processes && data.top_cpu_processes.length > 0) {
                    cpuDiv.innerHTML = data.top_cpu_processes.slice(0, 10).map(proc => 
                        `<div class="process-item">
                            <strong>${proc.Name || 'N/A'}</strong><br>
                            CPU: ${proc.CPU || 'N/A'}% | Memory: ${proc.WS || 'N/A'}
                        </div>`
                    ).join('');
                } else {
                    cpuDiv.textContent = 'No data';
                }
                
                const memDiv = document.getElementById('top-memory-processes');
                if (data.top_memory_processes && data.top_memory_processes.length > 0) {
                    memDiv.innerHTML = data.top_memory_processes.slice(0, 10).map(proc => 
                        `<div class="process-item">
                            <strong>${proc.Name || 'N/A'}</strong><br>
                            CPU: ${proc.CPU || 'N/A'}% | Memory: ${proc.WS || 'N/A'}
                        </div>`
                    ).join('');
                } else {
                    memDiv.textContent = 'No data';
                }
                
                const stockDiv = document.getElementById('stock-info');
                if (data.stock_info && data.stock_info.length > 0) {
                    stockDiv.innerHTML = data.stock_info.map(stock => 
                        `<div class="info-item">
                            <span class="info-label">${stock.name}</span>
                            <span class="info-value">${stock.code || 'N/A'}<br>Price: ${stock.price}<br>Source: ${stock.source}</span>
                        </div>`
                    ).join('');
                } else {
                    stockDiv.innerHTML = '<div class="info-item"><span class="info-value">No stock info</span></div>';
                }
                
            } catch (error) {
                console.error('Failed to load infos:', error);
            }
        }
        
        // Load all data
        async function loadAllData() {
            // Use relative paths for API calls
            await Promise.all([
                loadMemoStats(), // Load memo stats
                loadCurrentTemperature(),
                loadTemperatureHistory(),
                loadInterestingInfos()
            ]);
        }
        
        // Initial load
        loadAllData();
        
        // Auto-refresh every 30 seconds
        setInterval(loadAllData, 30000);
    </script>
</body>
</html>
    """
    
