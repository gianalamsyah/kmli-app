# ==========================================
# Serial Configuration
# ==========================================

SERIAL_PORT = "/dev/cu.usbserial-14120"
BAUDRATE = 230400

# ==========================================
# Race Configuration
# ==========================================

SLALOM_DISTANCE = 30.0      # meter

START_DISTANCE = 30          # S1 -> S2 (meter)
BRAKE_SENSOR_DISTANCE = 0.30   # S2 -> S3 (meter)

HILL_DISTANCE = 6.17      # meter
HILL_HEIGHT = 2.40        # meter
GRAVITY = 9.81            # m/s²

# ==========================================
# Race Mode
# ==========================================

MODE_START_FINISH = "START_FINISH"
MODE_LAP = "LAP"
MODE_BRAKE = "BRAKE"
MODE_HILL = "HILL_CLIMBING"
