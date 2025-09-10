print("--- START Loading file_bridge_api.py ---")
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, send_file, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import init_db, ChatSession, ChatMessage, SessionLocal, User, Base, engine, Memory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from uvicorn.middleware.wsgi import WSGIMiddleware
from flask_cors import CORS
from plugins.path_guard import is_allowed_path
import os, shutil, hashlib, json, toml, difflib, yaml, logging, time, subprocess, requests, base64, mimetypes, platform, fnmatch, pytz
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from datetime import datetime
from reportlab.pdfgen import canvas
from redbaron import RedBaron
from docx import Document
from pptx import Presentation
from openpyxl import Workbook
from plugins.docx_support import file_docx
from PIL import Image
from io import BytesIO
from plugins.binary_file_support import binary_api
from sentence_transformers import SentenceTransformer
import numpy as np
from smart_safe_write import smart_safe_write, auto_map_on_failure
from update_memory_context import update_memory_context
from plugins.safe_file_access import safe_open, safe_listdir, safe_isfile, safe_read
from plugins.safe_file_read import read_file_generic
from plugins.time_utils import get_local_timestamp
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, inspect, text # Add inspect
from cappy_validator import validate as validate_with_cappy

# [... Truncated for brevity ...]

# --- END NEW POSITION ---

if __name__ == "__main__":
    logger.info("Starting FileBridge in development mode")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)