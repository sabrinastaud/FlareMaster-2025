@echo off
if not defined IS_MINIMIZED (
    set IS_MINIMIZED=1
    start "" /min "%~dpnx0" %*
    exit
)

python -m streamlit run C:\Users\User\Desktop\Studium\Bachelorarbeit_MGST22\FlareMaster\ProgramCode_FlareMaster\PythonCode_FlareMaster\FlareAppMain.py
