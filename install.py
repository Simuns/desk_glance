#!/usr/bin/python3
import os
import shutil
import subprocess
import sys

def create_venv(venv_path):
    """Creates a virtual environment."""
    if not os.path.exists(venv_path):
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
    else:
        print("Virtual environment already exists.")

def install_requirements(venv_path):
    """Installs requirements using pip."""
    subprocess.check_call([os.path.join(venv_path, 'bin', 'pip'), 'install', '-r', 'requirements.txt'])

def generate_plist_content(python_executable_path, script_path):
    """Generates the plist content with specified paths."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.simuns.desk_glance</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_executable_path}</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/tmp/com.simuns.desk_glance.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/com.simuns.desk_glance.out</string>
</dict>
</plist>"""

def install():
    app_path = os.getcwd()
    venv_path = os.path.join(app_path, 'venv')

    # Create virtual environment and install requirements
    create_venv(venv_path)
    install_requirements(venv_path)

    venv_python_path = os.path.join(venv_path, 'bin', 'python')
    desk_glance_path = os.path.join(app_path, "desk_glance.py")

    plist_content = generate_plist_content(venv_python_path, desk_glance_path)
    plist_file_name = "com.simuns.desk_glance.plist"
    plist_path = os.path.join(app_path, plist_file_name)
    
    with open(plist_path, 'w') as plist_file:
        plist_file.write(plist_content)

    launch_agents_dir = os.path.expanduser('~/Library/LaunchAgents/')
    destination_plist_path = os.path.join(launch_agents_dir, plist_file_name)
    os.makedirs(launch_agents_dir, exist_ok=True)
    shutil.move(plist_path, destination_plist_path)

    os.chmod(desk_glance_path, 0o755)
    print("Installation complete. Please load the new agent with `launchctl load ~/Library/LaunchAgents/com.simuns.desk_glance.plist` or restart your computer.")

if __name__ == "__main__":
    install()
