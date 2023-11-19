from enum import Enum

class Mode(Enum):
    PROD = "prod"
    DEV = "dev"
    DEBUG = "debug"

def log(mode, message_dev, message_debug=None, message_prod=None):
    if mode == Mode.DEBUG:
        print(f"[debug] {message_debug}") if message_debug else print(f"[debug] {message_dev}")
    elif mode == Mode.DEV:
        print(f"[info] {message_dev}")
    elif message_prod:
        print(message_prod)
    
        