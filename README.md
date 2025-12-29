<p align="center">
  <img src="assets/banner.png" width="100%">
</p>

<h1 align="center">📱 QR CODE GENERATOR</h1>

<p align="center">
  <img src="assets/logo.png" width="180">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/PyQt6-GUI-green?style=for-the-badge&logo=qt">
  <img src="https://img.shields.io/badge/Database-JSON-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

---

# ⚠️ Aviso

**Status do Projeto:** Em desenvolvimento.

Um aplicativo desktop desenvolvido em **Python + PyQt6** para criação de **QR Codes**, incluindo:

- cores customizáveis  
- exportação para PNG e SVG  
- histórico salvo em JSON  
- visualização ampliada  

---

# ✅ Funcionalidades

### 🧾 Geração de QR Code
- Inserir texto ou link  
- Escolher cor principal e cor de fundo  
- QR Code gerado instantaneamente  

### 💾 Exportação
- Exportar como **PNG**  
- Exportar como **SVG (vetorial)**  

### 🗂 Histórico Avançado
- Armazenamento automático em **JSON**  
- Busca por texto  
- Visualização ampliada  
- Exclusão individual  
- Atualização automática  

### 🎨 Interface Moderna
- Estilo limpo  
- Botões estilizados  
- Campos arredondados  
- Experiência agradável em PyQt6  

---

# 🖼️ Capturas de Tela

## 🏠 Página Principal
<p align="center">
  <img src="assets/paginaprincipal.png" width="70%">
</p>

---

## 🎨 Seleção de Cores
<p align="center">
  <img src="assets/paleta.png" width="70%">
</p>

---

## 🗂 Histórico
<p align="center">
  <img src="assets/historico.png" width="70%">
</p>

---

## 🔍 Visualização Ampliada
<p align="center">
  <img src="assets/qrampliado.png" width="70%">
</p>

---

# 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|----------|------------|
| **Linguagem** | Python |
| **GUI** | PyQt6 |
| **Banco de Dados** | JSON |
| **Manipulação de Imagens** | Pillow |
| **QR Code** | qrcode |

---

# 🚀 Como Executar o Projeto

## 1️⃣ Clone o repositório
```bash
git clone https://github.com/MatheusPereiira/projeto-qr-code-generator-simples.git
cd projeto-qr-code-generator-simples
```
## 2️⃣ Crie um ambiente virtual
```bash
python -m venv venv
```

## ▶️ Ativar o ambiente virtual
```bash
Windows:
.\venv\Scripts\activate
```
## Linux/macOS:
```bash
source venv/bin/activate
```
## 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```
## 4️⃣ Execute o programa
```bash
python main.py
```
---

## 📂 Estrutura do Projeto
```bash
projeto_qrcode/
│
├── assets/                 # Imagens usadas no README
│   ├── banner.png
│   ├── logo.png
│   ├── paginaprincipal.png
│   ├── paleta.png
│   ├── historico.png
│   └── qrampliado.png
│
├── backend/
│   ├── database.py         # Manipulação do JSON
│   └── qrgenerator.py      # Geração do QR 
│
├── data/
│   └── history.json        # Histórico dos QR Codes
│
├── frontend/
│   ├── app.py              # Interface principal
│   ├── history_item.py     # Item individual do histórico
│   └── viewer.py           # Visualização ampliada
│
├── utils/
│   └── image_utils.py      # Funções auxiliares
│
├── main.py
├── requirements.txt
└── README.md
```
--- 

## 📄 Licença
Este projeto está sob a **MIT License**, permitindo uso livre para estudo, modificação e distribuição.

---

## 👤 Autor
**Matheus Pereira** <br> 
💻 Estudante de Engenharia de Software Faculdade de Nova Serrana <br>
⭐ Apaixonado por desenvolvimento desktop em Python <br>
🔗 GitHub: https://github.com/MatheusPereiira

---
