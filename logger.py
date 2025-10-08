import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file path with today's date
log_file = os.path.join(LOG_DIR, f"{datetime.today().strftime('%Y-%m-%d')}.log")

def logger(msg, mytype="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{mytype}] - {msg}"
    
    # print(log_line)  # Console output

    with open(log_file, "a") as f:
        f.write(log_line + "\n")
