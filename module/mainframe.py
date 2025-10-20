import serial
import time

# Adjust COM port and baudrate
ser = serial.Serial("COM5", 9600, timeout=1)


def send_at(command, delay=1):
    """Send AT command and read the response"""
    ser.write((command + "\r\n").encode())
    time.sleep(delay)
    response = ser.read_all().decode(errors="ignore")
    print(f">>> {command}")
    print(response.strip(), "\n")
    return response


# Basic test
send_at("AT")

# Read current configuration
send_at("AT+CPIN?")  # SIM status
send_at("AT+COPS?")  # Operator
send_at("AT+CSQ")  # Signal
send_at("AT+CREG?")  # Registration
send_at("AT+CMGF?")  # SMS mode
send_at("AT+CPMS?")  # SMS storage
send_at("AT+IPR?")  # Baud rate
send_at("ATE?")  # Echo
send_at("AT+CCLK?")  # Internal clock
send_at("AT+SAPBR=2,1")  # GPRS bearer info

ser.close()
