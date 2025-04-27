@echo off
echo Current path is : %~dp0
cd /d "%~dp0"
python crawl_data_bj_gov.py
pause