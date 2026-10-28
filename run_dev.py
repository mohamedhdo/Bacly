#!/usr/bin/env python3
"""
Development server runner for Bacly in AI Studio.
Accepts any flags from npm/vite scripts (such as --port 3000 --host 0.0.0.0)
and runs Django's runserver on 0.0.0.0:3000.
"""
import os
import sys

port = "3000"
host = "0.0.0.0"

args = sys.argv[1:]
i = 0
while i < len(args):
    arg = args[i]
    if arg == "--port" and i + 1 < len(args):
        port = args[i + 1]
        i += 2
    elif arg.startswith("--port="):
        port = arg.split("=")[1]
        i += 1
    elif arg == "--host" and i + 1 < len(args):
        host = args[i + 1]
        i += 2
    elif arg.startswith("--host="):
        host = arg.split("=")[1]
        i += 1
    else:
        i += 1

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bacly.settings")

from django.core.management import execute_from_command_line

addrport = f"{host}:{port}"
print(f"Starting Bacly Django Development Server on http://{addrport} ...")
execute_from_command_line(["manage.py", "runserver", addrport])
