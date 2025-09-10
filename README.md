<p align="center">
  <img src="writeguard-logo.png" width="280" alt="WriteGuard Logo">
</p># ✍️ WriteGuard v0.0.2

![GitHub release (latest by date)](https://img.shields.io/github/v/release/yourusername/writeguard)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/yourusername/writeguard/test.yml)
![License](https://img.shields.io/github/license/yourusername/writeguard)

Secure, versioned, and auditable file writes for AI agents, developers, and compliance-critical systems.

---

## 📦 Install
```bash
pip install writeguard
```
Or clone the repo:
```bash
git clone https://github.com/yourusername/writeguard.git
cd writeguard
./install_writeguard.sh
```

---

## 🧰 Features
- ✅ Smart-safe file writes (backup + diff)
- 🔍 Dry-run & preview
- 🔐 Pro-only: diff summary + audit log UI
- 🧩 Plugin system for DOCX, PDF, JSON
- 🐳 Docker + Fly.io support

---

## 🚀 Quick Start (CLI)
```bash
writeguard myfile.txt --content "Hello!" --dry-run --preview
```

---

## 🧪 Run Tests
```bash
python -m unittest discover -s app/v0.0.2/tests
```

---

## 💼 Pro Mode
Enable advanced features:
```bash
export WRITEGUARD_PRO_MODE=true
```

---

## 📄 License
MIT © 2025 Terry Simmons