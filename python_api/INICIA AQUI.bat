@echo off
REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Definir variáveis de ambiente
set PUSHINPAY_BASE = "https://api.pushinpay.com.br"
set PUSHINPAY_TOKEN = "62784|0VAlLudbixBdW5yjv5xijXrvxRztVrDg15y8bxo7a70ca885"

REM Abrir navegador
start "" http://127.0.0.1:5000

REM Executar servidor Flask
python pix.py

REM Pausar para manter janela aberta
pause
