@echo off
setlocal enabledelayedexpansion
title 智绘脑图 SmartBrainMap - 停止服务

echo.
echo  ================================================
echo     智绘脑图 SmartBrainMap - 停止服务
echo  ================================================
echo.

rem ============ 查找占用 8000 端口的进程 ============
set "PID_FOUND="
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8000" ^| findstr LISTENING') do set "PID_FOUND=%%p"

if not defined PID_FOUND (
    echo  未检测到占用 8000 端口的服务，可能已停止。
    echo.
    pause
    exit /b 0
)

echo  发现后端进程 PID: !PID_FOUND!，正在停止...
taskkill /F /PID !PID_FOUND!
if "!errorlevel!"=="0" (
    echo.
    echo  服务已停止，端口 8000 已释放。
) else (
    echo.
    echo  停止失败，请用任务管理器结束 PID !PID_FOUND! 对应的 python 进程。
)
echo.
pause
