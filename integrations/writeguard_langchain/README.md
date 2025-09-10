# 🔌 WriteGuard LangChain Tool

LangChain tool wrapper for the [WriteGuard](https://github.com/yourusername/writeguard) secure write API.

---

## 📦 Install
```bash
pip install writeguard_langchain
```

## 🚀 Usage
```python
from writeguard_langchain import writeguard_write

result = writeguard_write.run(
    filepath="notes.txt",
    content="Updated by LangChain tool.",
    reason="LangChain Agent"
)
print(result)
```

---

## 🌐 API Requirements
Make sure the WriteGuard API is running at:
```bash
http://localhost:5050/write
```

Enable Pro mode to use diff summaries in response:
```bash
export WRITEGUARD_PRO_MODE=true
```

---

MIT License © 2025 Terry Simmons