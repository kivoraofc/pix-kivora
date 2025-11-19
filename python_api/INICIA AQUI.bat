@echo off
REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Definir variáveis de ambiente
set PUSHINPAY_BASE = "https://api.pushinpay.com.br"
set PUSHINPAY_TOKEN = "43868|KDTirIabgqJOrQHPEeUzkja97Mx18xhlMf8JrQDnb8a5822a

REM Abrir navegador
start "" http://127.0.0.1:5000

REM Executar servidor Flask
python pix.py

REM Pausar para manter janela aberta
pause
