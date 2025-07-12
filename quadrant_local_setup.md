# 🔧 Running Qdrant Locally (Without Docker)

This guide provides step-by-step instructions to download, extract, and run the Qdrant vector database server locally on both **Linux** and **Windows** systems.

---

## ✅ Prerequisites

- `curl` installed
- `unzip` utility installed
- No Docker required
---

## 📥 1. Download Qdrant Binary

### For **Windows**:
Run the following in **CMD or PowerShell**:

```powershell
curl -L -o qdrant.zip "https://github.com/qdrant/qdrant/releases/latest/download/qdrant-windows-x86_64.zip"
```
For Linux:
Open the terminal and run:

```bash
curl -L -o qdrant.zip "https://github.com/qdrant/qdrant/releases/latest/download/qdrant-linux-x86_64.zip"
```
📦 2. Extract Qdrant
```bash
unzip qdrant.zip -d qdrant
cd qdrant
```
This creates a folder named qdrant with the necessary binary inside.

🚀 3. Run the Qdrant Server
On Linux:
```bash
./qdrant
```
On Windows:
```bash
qdrant.exe
```
🌐 Qdrant Web API

By default, Qdrant runs at:
```bash
📍 http://localhost:6333
```


#You can now access the REST API to:

Create collections

Upload vectors

Perform similarity search
