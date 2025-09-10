# 🤝 Contributing to WriteGuard

Thanks for your interest in contributing to **WriteGuard**!
Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

---

## 🛠 How to Contribute

1. **Fork the repo** and create a branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Write code + tests** in `app/v0.0.2/`

3. **Run tests** before pushing:
   ```bash
   python -m unittest discover -s app/v0.0.2/tests
   ```

4. **Open a pull request** with a clear description.

---

## 📦 Adding a Plugin
Plugins run after successful writes based on filetype.
To add a new one:
- Edit `_run_post_write_plugins()` in `smart_safe_write.py`
- Add a handler for your desired extension
- Follow the pattern used for `.docx`, `.pdf`, etc.

---

## 💬 Need Help?
Open an issue or start a discussion.

---

Happy writing – safely!

_Terry Simmons | MIT Licensed_