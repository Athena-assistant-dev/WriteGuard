# ✍️ WriteGuard v0.0.2

**WriteGuard** is a secure, versioned, and auditable file write system designed for developers, AI agents, and compliance-sensitive environments. It enforces smart-safe-write logic using file diffs, backups, hash verification, and rollback support.

---

## 🚀 Features
- 🔐 Safe file writes with validation, backup, and diff logging
- 🧪 Dry-run and preview modes
- 📜 Structured audit logs
- 🧩 Plugin hooks for post-write processing (PDF, DOCX, etc.)
- 🖥️ REST API and CLI included
- 🐳 Docker-ready deployment

---

## 🛠 Usage

### 📦 Docker Compose
```bash
docker-compose up --build
```

### 🌐 API (Flask)
```bash
curl -X POST http://localhost:5050/write \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "example.txt",
    "content": "New content!",
    "dry_run": true,
    "preview": true,
    "reason": "testing"
  }'
```

### 🖥️ CLI
```bash
python writeguard_cli.py example.txt --content "New content" --dry-run --preview
```

---

## 🔌 Plugin System
- Post-write plugins auto-run for `.docx`, `.pdf`, `.pptx`, `.xlsx`, and images
- Located inside `smart_safe_write.py` > `_run_post_write_plugins`
- Easily extensible — add handlers for custom types

---

## 📁 Config
Supports `.env` and `writeguard.yaml`:
- Limit file size
- Set protected file paths
- Configure diff sensitivity

---

## 📃 License
MIT License — see LICENSE file.

---

## 🧪 Test
```bash
python -m unittest tests/test_writeguard.py
```

---

## 🌍 Roadmap
- GUI diff viewer
- LangChain integration
- Git plugin
- SaaS hosted version (Fly.io / Render)

---

## 🤝 Contribute
Pull requests welcome. Please include tests for new functionality.

---

## 📫 Contact
Created by Terry Simmons • Follow @writesecure on GitHub or Twitter