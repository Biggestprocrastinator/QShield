# 🛡️ Requiem

### Quantum-Proof Cryptography Scanner

<p align="center">

  <a href="https://github.com/Biggestprocrastinator/Requiem">
    <img src="https://img.shields.io/github/stars/Biggestprocrastinator/Requiem?style=for-the-badge&logo=github" />
  </a>

  <a href="https://github.com/Biggestprocrastinator/Requiem/network">
    <img src="https://img.shields.io/github/forks/Biggestprocrastinator/Requiem?style=for-the-badge&logo=github" />
  </a>

  <img src="https://img.shields.io/github/license/Biggestprocrastinator/Requiem?style=for-the-badge" />

  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />

  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi" />

  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react" />

  <img src="https://img.shields.io/badge/Nuclei-Security-red?style=for-the-badge" />

  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />

</p>

---

## 🚀 Overview
<img src="https://img.shields.io/badge/PQC-Ready-purple?style=for-the-badge" />
<img src="https://img.shields.io/badge/Cyber-Rating-orange?style=for-the-badge" />
<img src="https://img.shields.io/badge/CBOM-Enabled-black?style=for-the-badge" />
**Requiem** is a next-generation **cryptographic intelligence and asset discovery platform** designed to analyze enterprise infrastructure for **security vulnerabilities and post-quantum cryptography readiness**.

It combines **reconnaissance, cryptographic analysis, and vulnerability scanning** into a unified dashboard.


---

## ✨ Features

### 🔍 Asset Discovery

* Subdomain enumeration using **Subfinder**
* Certificate-based discovery using **crt.sh**
* Real-time asset inventory generation

---

### 🌐 Live Host Detection

* Fast probing using **httpx**
* DNS resolution + filtering of active assets

---

### 🔓 Vulnerability Scanning

* On-demand scanning using **Nuclei**
* Focused detection of **High & Critical vulnerabilities**

---

### 🔐 Cryptographic Analysis (CBOM)

* TLS version detection
* Cipher suite identification
* Key algorithm & key size extraction
* Certificate authority & expiry tracking

---

### 🧠 PQC Risk Assessment

* Detects non-quantum-safe algorithms (RSA, ECC)
* Flags cryptographic weaknesses
* Evaluates future quantum risk exposure

---

### 📊 Cyber Rating Engine

* Aggregates:

  * Vulnerabilities
  * Cryptographic posture
  * Certificate risks
* Generates an overall **security rating**

---

## 🏗️ Tech Stack

| Layer    | Technology       |
| -------- | ---------------- |
| Backend  | FastAPI, Python  |
| Frontend | React, HTML, CSS |
| Database | SQLAlchemy       |
| Recon    | Subfinder, httpx |
| Scanning | Nmap, Nuclei     |
| Crypto   | SSLyze, OpenSSL  |

---

## ⚙️ Installation & Setup

### 📌 Prerequisites

* Python 3.10+
* Node.js 18+
* Nmap installed system-wide
  👉 https://nmap.org/download.html

---

### 🖥️ Backend Setup

```bash
cd qshield-backend

# Create virtual environment
python -m venv .venv

# Activate environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn backend.app.main:app --reload
```

---

### 🌐 Frontend Setup

```bash
cd qshield-backend/frontend

npm install
npm run dev
```

---

## 🧪 Usage

1. Enter a domain (e.g., `example.com`)
2. Run asset discovery
3. View:

   * Live assets
   * TLS & cryptographic details
   * Certificate intelligence
4. Optionally run **Nuclei scan**
5. Analyze:

   * Vulnerabilities
   * PQC readiness
   * Cyber rating

---

## 📸 Key Modules

* 🧾 **Assets Dashboard** – Full asset + certificate intelligence
* 🔐 **CBOM** – Cryptographic Bill of Materials
* ⚠️ **Vulnerability Scan** – Nuclei-powered findings
* 🧠 **PQC Posture** – Quantum readiness insights

---

## 🛠️ Roadmap

* [ ] Async pipeline optimization
* [ ] Real-time scan progress tracking
* [ ] Advanced risk scoring engine
* [ ] Authentication & role-based access
* [ ] Cloud deployment

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a PR.

---

## 📜 License

This project is licensed under the MIT License.

---

## 💡 Inspiration

Built to address the growing need for **quantum-ready security analysis** and unified visibility into enterprise cryptographic posture.

---

<p align="center">
  ⚡ Built for Security • Designed for Scale • Ready for the Quantum Era ⚡
</p>
