@echo off
setlocal

rem Se coloca en la carpeta donde esta este .bat, para que
rem "python -m reflex run" se ejecute siempre en el sitio correcto.
cd /d "%~dp0"

echo Activando entorno conda "reflex"...
call conda activate reflex

if errorlevel 1 (
    echo.
    echo [ERROR] No se ha podido activar el entorno "reflex".
    echo Comprueba que:
    echo   1^) Tienes Anaconda o Miniconda instalado.
    echo   2^) Existe un entorno llamado "reflex" ^(conda env list^).
    echo   3^) Has ejecutado una vez: conda init cmd.exe
    echo      ^(y has reiniciado la terminal despues^)
    echo.
    pause
    exit /b 1
)

echo Entorno activado. Lanzando Reflex...
echo.
python -m reflex run

echo.
echo La aplicacion se ha detenido.
pause