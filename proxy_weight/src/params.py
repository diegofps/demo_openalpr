import os


APP_NAME           = os.getenv("APP_NAME", "openalpr")
CLIENT_CRT         = os.getenv("CLIENT_CRT", "../keys/client-admin.crt")
CLIENT_KEY         = os.getenv("CLIENT_KEY", "../keys/client-admin.key")
SERVER_CRT         = os.getenv("SERVER_CRT", "../keys/server-ca.crt")
SSH_USER           = os.getenv("SSH_USER", "ngd")
SSH_PRIVATE_KEY    = os.getenv("SSH_PRIVATE_KEY", "../keys/id_rsa")
API_SERVER         = os.getenv("API_SERVER", "https://192.168.1.134:6443")
STRATEGY           = os.getenv("STRATEGY", "WEIGHT")
NUM_THREADS        = int(os.getenv("NUM_THREADS", "16"))
REFRESH_SECONDS    = int(os.getenv("REFRESH_SECONDS", "3"))
MIN_CPU_FOR_WEIGHT = float(os.getenv("MIN_CPU_FOR_WEIGHT", "0.9"))
MOVING_AVERAGE_LEN = int(os.getenv("MOVING_AVERAGE_LEN", "1"))
ON_BUSY            = os.getenv("ON_BUSY", "1") != "0"
TIME_TO_WEIGHT     = os.getenv("TIME_TO_WEIGHT", "time_to_weight_3")
