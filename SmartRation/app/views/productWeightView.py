# import serial
import subprocess
import re
import serial
from django.shortcuts import render
from django.http import JsonResponse


arduino = None
com_port = None

def find_arduino_in_com_ports():
    for i in range(1, 11):  # COM1 to COM10
        port = f'COM{i}'
        try:
            test = serial.Serial(port, 9600, timeout=1)
            print(f"Connected to {port}")
            test.close()
            return port
        except (serial.SerialException, OSError):
            pass
    return None

def initial_setup(request):
    global arduino, com_port  # ⬅️ declare as global

    com_port = find_arduino_in_com_ports()
    if com_port is None:
        return JsonResponse({'error': 'No Arduino found'}, status=404)

    if arduino is not None:
        arduino.close()

    try:
        arduino = serial.Serial(com_port, 9600, timeout=1)
        return JsonResponse({'message': f'Arduino connected on {com_port}'})
    except serial.SerialException as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_weight(request):
    print(find_arduino_in_com_ports())
    try:
        weight = arduino.readline().decode().strip()
        print(weight)
        return JsonResponse({'weight': weight})
    except Exception as e:
        return JsonResponse({'error': ""})

def find_arduino_port():
    ports = list(mySerial.comports())
    for port in ports:
        if 'Arduino' in port.description or 'ttyUSB' in port.device or 'ttyACM' in port.device:
            return port.device  # e.g., '/dev/ttyACM0' or 'COM3'
    return None

def find_arduino_port_windows():
    try:
        output = subprocess.check_output(['wmic', 'path', 'Win32_SerialPort'], universal_newlines=True)
        for line in output.split('\n'):
            if 'Arduino' in line:
                match = re.search(r'(COM\d+)', line)
                if match:
                    return match.group(1)
    except Exception as e:
        print("Error:", e)
    return None

def display_html(request):
    print(find_arduino_port())
    """Render the HTML page for weight load."""
    return render(request, "weightLoad.html")

def display_html1(request):
    """Render the HTML page for weight load."""
    return render(request, "weightLoad1.html")
