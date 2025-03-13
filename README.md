# Premiumy\_TT

## 📌 Project Setup Guide (Linux)

### 📢 Requirements

- **Python**: 3.12
- **Poetry**: Dependency management tool
- **Google Chrome**: Link for download:
https://drive.google.com/file/d/1PK6g2w3jbs6ekK62c-Y5yvYbIxZ54EKO/view?usp=sharing
- **.env File**: Put this file and Google Chrome to directory with main.py
---

## 🚀 Installation Steps

### 1️⃣ Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Verify installation:**

```bash
poetry --version
```

### 2️⃣ Install Dependencies

```bash
poetry install
```

### 3️⃣ Install Google Chrome

```bash
sudo apt update
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
```

**Verify installation:**

```bash
google-chrome --version
```

### 4️⃣ Activate Virtual Environment

```bash
source .venv/bin/activate
```

### 5️⃣ Run the Project

```bash
python main.py
```

### 🎯 Expected Result

A screenshot named \`success.png\` should be generated.

