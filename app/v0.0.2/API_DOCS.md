# 📘 WriteGuard API Docs (v0.0.2)

## 🔄 POST `/write`
Safely writes content to a file with verification, diffing, and optional preview/dry-run.

### Request Body (JSON)
```json
{
  "filepath": "string",
  "content": "string",
  "override": "boolean (optional)",
  "reason": "string",
  "mode": "string (optional, default: 'default')",
  "dry_run": "boolean",
  "preview": "boolean"
}
```

### Response (JSON)
```json
{
  "status": "success | dry_run | error",
  "filepath": "string",
  "diff": ["- old line", "+ new line"],
  "backup": "string (path)",
  "hash": "string (sha256)"
}
```

---

## 🌐 Running the API
```bash
python writeguard_api.py
```

Accessible by default at `http://localhost:5050/write`

---

## 🔧 Plugin System
Plugins auto-run after safe writes:
- `.docx`, `.pdf`, `.pptx`, `.xlsx`, image formats

Customize by editing `_run_post_write_plugins()` in `smart_safe_write.py`

---

## 🔐 Config Reference
**From `.env`**:
- `BASE_PATH`
- `PORT`
- `ENABLE_IMMUTABLE_PROTECTION`

**From `writeguard.yaml`**:
```yaml
writeguard:
  default_mode: default
  log_level: INFO
  limits:
    max_file_size_kb: 2560
    max_diff_lines: 500
  protected_files:
    - /srv/system/config.yaml
```

---

## 🧪 Example: Dry Run with Diff Preview
```bash
curl -X POST http://localhost:5050/write \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "test.json",
    "content": "{\"a\": 1}",
    "dry_run": true,
    "preview": true,
    "reason": "test"
  }'
```

---

## 🆘 Troubleshooting
- Returns `400` if `filepath` or `content` is missing
- Handles protected file exceptions with status: `error`
- Check logs in `/srv/logs` or console output