@echo off

cd /d "%~dp0"

call .venv\Scripts\activate

start http://localhost:8501

timeout /t 2 >nul

python -m streamlit run app\app.py