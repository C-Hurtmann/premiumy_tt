# Premiumy\_TT

## 📌 Project Setup Guide (Linux)

### 📢 Requirements

- **Python**: 3.12
- **Poetry**: Dependency management tool
- **Google Chrome**: Required for automation

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

A screenshot named \`\` should be generated.

---

✅ **You’re all set!** 🎉 If you encounter any issues, feel free to check dependencies and retry the steps.

