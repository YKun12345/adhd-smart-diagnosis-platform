@echo off
setlocal enabledelayedexpansion
title 智绘脑图 SmartBrainMap - 一键启动

rem ============================================
rem  定位项目根目录：本脚本位于项目根/.claude 下，
rem  上一级即为项目根目录
rem ============================================
cd /d "%~dp0.."

echo.
echo  ================================================
echo     智绘脑图 SmartBrainMap - 一键启动
echo     后端入口 : http://127.0.0.1:8000
echo     前端页面 : http://127.0.0.1:8000/login.html
echo  ================================================
echo.

rem ============ 检查虚拟环境 ============
if not exist ".venv\Scripts\python.exe" (
    echo  [错误] 未找到虚拟环境 .venv，无法启动。
    echo         请先按本目录下的《启动说明.md》创建环境并安装依赖。
    echo.
    pause
    exit /b 1
)

rem ============ 检查端口 8000 是否被占用 ============
set "PORT_BUSY=0"
for /f "delims=" %%i in ('netstat -ano ^| findstr LISTENING ^| findstr ":8000"') do set "PORT_BUSY=1"
if "!PORT_BUSY!"=="1" (
    echo  [提示] 端口 8000 已有服务在监听，可能后端已在运行。
    echo         如果只是要打开页面，请直接访问：
    echo             http://127.0.0.1:8000/login.html
    echo         如需重启后端，请先关闭占用 8000 的进程，再运行本脚本。
    echo.
    pause
    exit /b 1
)

rem ============ 自动打开浏览器并启动后端 ============
echo  正在启动后端服务... （关闭本窗口或按 Ctrl+C 即可停止）
echo.
start "" "http://127.0.0.1:8000/login.html"
".venv\Scripts\python.exe" -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

echo.
echo  服务已停止。
pause
