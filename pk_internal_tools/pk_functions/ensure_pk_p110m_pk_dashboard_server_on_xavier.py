#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xavier에서 실행되는 멀티 데이터 대시보드 서버

이 파일은 Xavier에서 직접 실행되며, P110M, TV, Arduino 등 여러 데이터 소스를 조회/제어할 수 있는 통합 웹 대시보드를 제공합니다.
"""
import sys
import os
from pathlib import Path
import uvicorn
import logging
import socket
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict

# 프로젝트 로깅 초기화
try:
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
    ensure_pk_log_initialized(__file__)
except Exception:
    # Xavier에서 프로젝트 경로가 없을 경우 기본 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] [%(message)s]'
    )

logger = logging.getLogger(__name__)

# Xavier의 DB 경로 설정
db_dir = Path.home() / "pk_system" / ".pk_system"
db_dir.mkdir(parents=True, exist_ok=True)
db_path = db_dir / "pk_system.sqlite"

# 환경 변수로 DB 경로 설정 (대시보드 서버에서 사용)
os.environ["pk_SQLITE_PATH"] = str(db_path)

# 프로젝트 경로 추가 (Xavier의 pk_system 루트경로)
pk_root = Path.home() / "pk_system"
if (pk_root / "pk_internal_tools").exists():
    sys.path.insert(0, str(pk_root))
    sys.path.insert(0, str(pk_root / "pk_internal_tools"))

try:
    # FastAPI 앱 생성
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import HTMLResponse, JSONResponse
    import sqlite3
    
    app = FastAPI(title="Multi Data Dashboard (Xavier)", version="1.0.0")
    
    # P110M 에너지 히스토리 조회 함수
    def get_p110m_energy_history_from_db(device_host=None, days=365, limit=None):
        """DB에서 P110M 에너지 히스토리 조회"""
        try:
            if not db_path.exists():
                logger.debug("DB 파일이 존재하지 않습니다: %s", db_path)
                return []
            
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            cutoff_time = datetime.now() - timedelta(days=days)
            
            query = """
                SELECT device_host, current_power, today_energy, today_runtime,
                       month_energy, month_runtime, local_time, collected_at
                FROM p110m_energy_data 
                WHERE collected_at >= ?
            """
            params = [cutoff_time.isoformat()]
            
            if device_host:
                query += " AND device_host = ?"
                params.append(device_host)
            
            query += " ORDER BY collected_at DESC"
            
            if limit:
                query += f" LIMIT {limit}"
            
            cur.execute(query, params)
            rows = cur.fetchall()
            conn.close()
            
            result = []
            for row in rows:
                local_time = None
                if row['local_time']:
                    try:
                        local_time = datetime.fromisoformat(row['local_time'].replace('Z', '+00:00'))
                    except Exception:
                        pass
                
                collected_at = None
                if row['collected_at']:
                    try:
                        collected_at = datetime.fromisoformat(row['collected_at'].replace('Z', '+00:00'))
                    except Exception:
                        collected_at = datetime.now()
                else:
                    collected_at = datetime.now()
                
                result.append({
                    'device_host': row['device_host'],
                    'current_power': row['current_power'],
                    'today_energy': row['today_energy'],
                    'today_runtime': row['today_runtime'],
                    'month_energy': row['month_energy'],
                    'month_runtime': row['month_runtime'],
                    'local_time': local_time,
                    'collected_at': collected_at
                })
            
            logger.debug("에너지 히스토리 조회 완료: %d개 레코드", len(result))
            return result
        except Exception as e:
            logger.error("에너지 히스토리 조회 실패: %s", e, exc_info=True)
            return []
    
    # P110M 에너지 집계 함수
    def get_p110m_energy_aggregated_for_graph(device_host=None, period="year"):
        """P110M 에너지 데이터 집계"""
        try:
            days_map = {"day": 1, "week": 7, "month": 30, "year": 365}
            days = days_map.get(period, 365)
            
            history_data = get_p110m_energy_history_from_db(device_host=device_host, days=days, limit=None)
            
            if not history_data:
                logger.debug("집계할 에너지 데이터가 없습니다.")
                return []
            
            aggregated = defaultdict(lambda: {
                'total_energy': 0.0,
                'power_values': [],
                'total_runtime': 0,
                'data_points': 0
            })
            
            for record in history_data:
                date_key = None
                if record.get('collected_at'):
                    date_key = record['collected_at'].date().isoformat()
                elif record.get('local_time'):
                    if isinstance(record['local_time'], datetime):
                        date_key = record['local_time'].date().isoformat()
                    elif isinstance(record['local_time'], str):
                        try:
                            date_key = datetime.fromisoformat(record['local_time']).date().isoformat()
                        except Exception:
                            continue
                else:
                    continue
                
                if not date_key:
                    continue
                
                if record.get('today_energy') is not None:
                    aggregated[date_key]['total_energy'] = max(
                        aggregated[date_key]['total_energy'],
                        record.get('today_energy', 0.0) or 0.0
                    )
                
                if record.get('current_power') is not None:
                    power = record.get('current_power', 0.0) or 0.0
                    aggregated[date_key]['power_values'].append(power)
                
                if record.get('today_runtime') is not None:
                    aggregated[date_key]['total_runtime'] = max(
                        aggregated[date_key]['total_runtime'],
                        record.get('today_runtime', 0) or 0
                    )
                
                aggregated[date_key]['data_points'] += 1
            
            result = []
            for date_key in sorted(aggregated.keys()):
                data = aggregated[date_key]
                
                avg_power = 0.0
                max_power = 0.0
                if data['power_values']:
                    avg_power = sum(data['power_values']) / len(data['power_values'])
                    max_power = max(data['power_values'])
                
                result.append({
                    'date': date_key,
                    'total_energy': data['total_energy'],
                    'avg_power': avg_power,
                    'max_power': max_power,
                    'total_runtime': data['total_runtime'],
                    'data_points': data['data_points']
                })
            
            logger.debug("에너지 데이터 집계 완료: %d개 날짜", len(result))
            return result
        except Exception as e:
            logger.error("에너지 집계 실패: %s", e, exc_info=True)
            return []
    
    # API 엔드포인트
    @app.get("/")
    async def dashboard_home():
        """대시보드 메인 페이지"""
        html_content = get_dashboard_html()
        return HTMLResponse(content=html_content)
    
    @app.get("/api/p110m/energy/history")
    async def get_p110m_energy_history(device_host: Optional[str] = None, days: int = 365, limit: Optional[int] = None):
        """P110M 에너지 히스토리 조회"""
        try:
            history = get_p110m_energy_history_from_db(device_host=device_host, days=days, limit=limit)
            result = [
                {
                    "device_host": item["device_host"],
                    "current_power": item["current_power"],
                    "today_energy": item["today_energy"],
                    "month_energy": item["month_energy"],
                    "collected_at": item["collected_at"].isoformat() if isinstance(item["collected_at"], datetime) else str(item.get("collected_at", "")),
                    "local_time": item["local_time"].isoformat() if isinstance(item.get("local_time"), datetime) else str(item.get("local_time", ""))
                }
                for item in history
            ]
            return JSONResponse(content=result)
        except Exception as e:
            logger.error("P110M 에너지 히스토리 조회 실패: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/p110m/energy/aggregated")
    async def get_p110m_energy_aggregated(device_host: Optional[str] = None, period: str = "year"):
        """P110M 에너지 데이터 집계"""
        try:
            aggregated = get_p110m_energy_aggregated_for_graph(device_host=device_host, period=period)
            return JSONResponse(content=aggregated)
        except Exception as e:
            logger.error("P110M 에너지 집계 조회 실패: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/p110m/control")
    async def control_p110m(action: str, device_host: Optional[str] = None):
        """P110M 제어 (on, off, toggle, info, energy)"""
        try:
            # TODO: Xavier에서 직접 P110M 제어 구현
            # 현재는 기본 응답만 반환
            result = {"status": "success", "action": action, "message": f"P110M {action} 명령 실행됨"}
            return JSONResponse(content=result)
        except Exception as e:
            logger.error("P110M 제어 실패: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_dashboard_html():
        """대시보드 HTML 템플릿"""
        return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi Data Dashboard (Xavier)</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 12px;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: white;
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .header h1 { color: #667eea; margin-bottom: 8px; }
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .chart-container h2 { color: #667eea; margin-bottom: 16px; }
        #energy-chart { height: 400px; width: 100%; }
        .control-panel {
            background: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .control-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            margin: 4px;
            font-size: 16px;
        }
        .control-btn:hover { background: #5568d3; }
        .control-btn:active { transform: scale(0.98); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 멀티 데이터 대시보드 (Xavier)</h1>
            <div id="current-time"></div>
            <button class="control-btn" onclick="loadEnergyData()">🔄 새로고침</button>
        </div>
        
        <div class="control-panel">
            <h2>🔌 P110M 제어</h2>
            <button class="control-btn" onclick="controlP110m('on')">켜기</button>
            <button class="control-btn" onclick="controlP110m('off')">끄기</button>
            <button class="control-btn" onclick="controlP110m('toggle')">토글</button>
            <button class="control-btn" onclick="controlP110m('info')">정보</button>
            <button class="control-btn" onclick="controlP110m('energy')">에너지</button>
        </div>
        
        <div class="chart-container">
            <h2>📈 에너지 사용량</h2>
            <select id="energy-period" onchange="loadEnergyData()" style="padding: 8px; border-radius: 8px; margin-bottom: 12px;">
                <option value="year">1년</option>
                <option value="month">1개월</option>
                <option value="week">1주일</option>
                <option value="day">1일</option>
            </select>
            <div id="energy-chart"></div>
        </div>
    </div>
    
    <script>
        function updateCurrentTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = 
                now.toLocaleString('ko-KR');
        }
        setInterval(updateCurrentTime, 1000);
        updateCurrentTime();
        
        async function loadEnergyData() {
            try {
                const period = document.getElementById('energy-period').value;
                const response = await fetch(`/api/p110m/energy/aggregated?period=${period}`);
                const data = await response.json();
                
                if (data.length === 0) {
                    document.getElementById('energy-chart').innerHTML = 
                        '<div style="text-align: center; padding: 40px;">데이터가 없습니다.</div>';
                    return;
                }
                
                const dates = data.map(d => d.date);
                const energies = data.map(d => d.total_energy);
                
                const trace = {
                    x: dates,
                    y: energies,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: '에너지 사용량',
                    line: { color: '#667eea', width: 2 },
                    marker: { size: 6 }
                };
                
                const layout = {
                    title: 'P110M 에너지 사용량',
                    xaxis: { title: '날짜' },
                    yaxis: { title: '에너지 (Wh)' },
                    responsive: true
                };
                
                Plotly.newPlot('energy-chart', [trace], layout, {responsive: true});
            } catch (error) {
                console.error('에너지 데이터 로드 실패:', error);
                document.getElementById('energy-chart').innerHTML = 
                    '<div style="text-align: center; padding: 40px; color: red;">데이터를 불러올 수 없습니다.</div>';
            }
        }
        
        async function controlP110m(action) {
            try {
                const response = await fetch(`/api/p110m/control?action=${action}`, {
                    method: 'POST'
                });
                const data = await response.json();
                alert(`P110M 제어: ${data.message}`);
                if (action === 'energy') {
                    loadEnergyData();
                }
            } catch (error) {
                console.error('P110M 제어 실패:', error);
                alert('제어 실패: ' + error.message);
            }
        }
        
        // 초기 로드
        loadEnergyData();
        setInterval(loadEnergyData, 60000); // 1분마다 자동 새로고침
    </script>
</body>
</html>
        """
    
    # 서버 시작
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    
    # 호스트와 포트는 명령줄 인자 또는 환경 변수에서 가져오기
    host = os.environ.get("MULTI_DATA_DASHBOARD_HOST", "0.0.0.0")
    port = int(os.environ.get("MULTI_DATA_DASHBOARD_PORT", "8000"))
    
    logger.info("=" * 60)
    logger.info("📊 멀티 데이터 대시보드 서버 시작 (Xavier)")
    logger.info("=" * 60)
    logger.info("📱 모바일 접속: http://%s:%d", local_ip, port)
    logger.info("💻 PC 접속: http://localhost:%d", port)
    logger.info("🌐 네트워크 접속: http://%s:%d", local_ip, port)
    logger.info("📊 DB 경로: %s", db_path)
    logger.info("=" * 60)
    logger.info("서버를 중지하려면 Ctrl+C를 누르세요.")
    logger.info("=" * 60)
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
except Exception as e:
    logger.error("대시보드 서버 시작 실패: %s", e, exc_info=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

