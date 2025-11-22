"""
Imports centralizados para evitar duplicação
Apenas módulos essenciais disponíveis
"""

# Python standard library
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from decimal import Decimal
import os
import io
import json
import logging
import time
import random
import functools

# Flask core
from flask import Flask, render_template, request, redirect, url_for, flash, abort, current_app, jsonify, send_file

# Flask extensions (essenciais)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# SQLAlchemy core
from sqlalchemy import text, Index, CheckConstraint
from sqlalchemy.orm import relationship

# Security
from werkzeug.security import generate_password_hash, check_password_hash

# Environment
from dotenv import load_dotenv

# Logging
from logging.handlers import RotatingFileHandler

# Exportar tudo para uso em outros módulos
__all__ = [
    # Standard library
    'datetime', 'date', 'timedelta', 'Optional', 'List', 'Dict', 'Any', 'Decimal',
    'os', 'io', 'json', 'logging', 'time', 'random', 'functools',
    
    # Flask
    'Flask', 'render_template', 'request', 'redirect', 'url_for', 
    'flash', 'abort', 'current_app', 'jsonify', 'send_file',
    
    # Flask extensions
    'SQLAlchemy', 'CORS',
    
    # SQLAlchemy
    'text', 'Index', 'CheckConstraint', 'relationship',
    
    # Security
    'generate_password_hash', 'check_password_hash',
    
    # Environment
    'load_dotenv', 'RotatingFileHandler'
]
