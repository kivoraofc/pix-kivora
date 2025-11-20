# 🚀 GERADOR PIX KIVORA

## Descrição
Este projeto é um gerador de cobranças PIX desenvolvido com Flask e JavaScript. Ele permite que os usuários escolham valores pré-definidos ou insiram valores personalizados para gerar QR Codes e copiar chaves PIX.

## Funcionalidades
- 💳 **Gerador de PIX**: Escolha valores ou insira um valor personalizado (R$1 a R$150).
- 📋 **Copiar chave PIX**: Copie a chave gerada diretamente para a área de transferência.
- 📱 **Responsivo**: Interface adaptada para dispositivos móveis e desktop.

## Tecnologias Utilizadas
- 🐍 **Backend**: Flask (Python)
- 🌐 **Frontend**: HTML, CSS e JavaScript
- 📦 **Deploy**: Render

## Passo a Passo para Configuração

### 1️⃣ Clonar o repositório
```bash
# Clone o repositório
git clone https://github.com/kivoraofc/pix-kivora.git
cd pix-flask-app
```

### 2️⃣ Instalar dependências
Certifique-se de ter o Python instalado.
```bash
# Instale as dependências
pip install -r python_api/requirements.txt
```

### 3️⃣ Executar localmente
```bash
# Inicie o servidor Flask
python python_api/pix.py
```
Acesse o aplicativo em `http://127.0.0.1:5000`.

### 4️⃣ Deploy no Render
1. Acesse [Render](https://dashboard.render.com).
2. Conecte sua conta GitHub e selecione o repositório.
3. Configure:
   - **Build Command**: `pip install -r python_api/requirements.txt`
   - **Start Command**: `gunicorn --chdir python_api pix:app`

## Estrutura do Projeto
```
├── api/
│   ├── pix/
│   │   ├── cashin.js
│   │   └── transactions/
├── public/
│   └── index.html
├── python_api/
│   ├── app.py
│   ├── pix.py
│   ├── requirements.txt
│   └── status.py
└── README.md
```

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).
