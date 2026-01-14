import os
import subprocess

cmd = "ls " + os.getenv("USER_INPUT", "")
subprocess.run(cmd, shell=True)  # semgrep часто ругается на shell=True
