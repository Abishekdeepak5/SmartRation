import serial
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from app.views import RationView
from app.dao.FamilyDao import getFamilyById
from app.dao.RationDao import *
from app.common.Util import get_current_date

arduino = None
com_port = None
collected_data = []

def find_arduino_in_com_ports():
    '''
    for i in range(1, 11):
        port = f'COM{i}'
        try:
            test = serial.Serial(port, 9600, timeout=1)
            test.close()
            return port
        except (serial.SerialException, OSError):
            pass
    return None
    '''
    return "COM8"

@csrf_exempt
def init_setup(request):
    global arduino, com_port, collected_data
    com_port = find_arduino_in_com_ports()
    collected_data = []
    if com_port is None:
        return JsonResponse({'error': 'Arduino not found'}, status=404)
    try:
        arduino = serial.Serial(com_port, 9600, timeout=1)
        return JsonResponse({'message': 'Arduino connected', 'port': com_port})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def read_weight(request):
    global arduino, com_port
    if arduino is None:
        if com_port is None:
            return JsonResponse({'error': 'COM port not available'}, status=400)
        try:
            arduino = serial.Serial(com_port, 9600, timeout=1)
        except Exception as ex:
            print("Failed to connect to Arduino:", ex)
            return JsonResponse({'error': 'Arduino not initialized'}, status=400)

    try:
        arduino.reset_input_buffer()  # Clear previous buffer
        weight_str = arduino.readline().decode().strip()
        print(weight_str)
        if weight_str == "":
            return JsonResponse({'WEIGHT':0})
        return JsonResponse({'weight':weight_str})
    except Exception as ex:
        print("Error reading weight:", ex)
        com_port = find_arduino_in_com_ports()
        try:
            arduino.close()
        except Exception as close_ex:
            print("Error closing Arduino:", close_ex)
        arduino = None  # Reset connection

        # Optional: attempt reconnect
        try:
            if com_port:
                arduino = serial.Serial(com_port, 9600, timeout=1)
        except Exception as reconnect_ex:
            print("Reconnect failed:", reconnect_ex)
        
        return JsonResponse({'error': f'Failed to read weight: {ex}'}, status=500)

@csrf_exempt
def submit_weight(request):
    global arduino, collected_data
    data = json.loads(request.body)
    collected_data.append(data)
    return JsonResponse({'message': 'Weight stored'})

@csrf_exempt
def finish(request,family_id):
    print(family_id)
    global arduino
    data = json.loads(request.body)
    distributeProduct=RationView.get_distribute_product(request)
    rationProducts=RationView.get_ration_product(request)
    family=getFamilyById(family_id)
    distributedProductsDetail = ""
    rationDetail = RationView.get_ration_detail(request)
    html_table_rows=""
    for rationProduct in data:
        ration_stock_quantity = rationProduct["stock_quantity"]
        distribute_quantity = distributeProduct[str(rationProduct["product_id"])]
        new_quantity = float(ration_stock_quantity) - float(distribute_quantity)
        if distribute_quantity != 0 and (new_quantity > 0):
            rationProductObj = RationProduct()
            rationProductObj.set_ration_product_id(rationProduct["ration_product_id"])
            rationProductObj.set_product_id(rationProduct["product_id"])
            rationProductObj.set_ration_id(rationProduct["ration_id"])
            rationProductObj.set_last_update(get_current_date())
            rationProductObj.set_stock_quantity(new_quantity)
            updateRationProduct(rationProductObj)
            
            rationFamily=RationFamily.RationFamily()
            rationFamily.set_product_id(rationProductObj.get_product_id())
            rationFamily.set_actual_quantity(distribute_quantity)
            rationFamily.set_family_id(family_id)
            rationFamily.set_issued_date(get_current_date())
            rationFamily.set_issued_quantity(rationProduct["issued_quantity"])
            rationFamily.set_ration_id(rationProductObj.get_ration_id())
            addProductsToFamily(rationFamily)
            
            html_table_rows += f"<tr><td>{rationProduct['product']['product_name']}</td><td>{rationProduct['product']['unit']}</td><td>{rationProduct['product']['price']}</td><td>{distribute_quantity}</td><td>{rationProduct['issued_quantity']}</td></tr>"
    html_table = RationView.form_html_table(html_table_rows)
    body = rationDetail+"<h1>குடும்பம் பெற்ற பொருட்களின் விவரம் (Family received product details)</h1>"+html_table
    body = body+"""
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSfKduKNfD9RNJTgR7sL63K8LrV1ReHjDLtAQewqSda-qLHTsQ/viewform?usp=header" style="font-size:16px; font-family: Arial, sans-serif; padding:10px 20px; border:none; border-radius:5px; background-color:#007BFF; color:#fff; cursor:pointer;">
             புகார் (Issue)
        </a>
        """
    html_code = RationView.form_html_code(body)
    RationView.send_custom_html_email(subject="இன்று ரேஷன் கடை திறந்திருக்கும்!",html=html_code,to_emails=[family['email']])
    if arduino:
        arduino.close()
        arduino = None
    print(data)
    # return redirect("list_ration_families")
    return JsonResponse({'message': 'Connection closed', 'data': collected_data})

from django.shortcuts import render

def weight_page(request):
    products = [
        {'ration_product_id': 6, 'ration_id': 2, 'product_id': 4, 'stock_quantity': 103.0, 'last_update': '2025-05-11', 'product': {'unit': 'Kg', 'price': 50.0, 'tolerance': 0.1, 'product_id': 4, 'last_update': '2025-04-28', 'product_name': 'Sugar', 'stock_quantity': 80}, 'distribute_quantity': 2.0},
        {'ration_product_id': 4, 'ration_id': 2, 'product_id': 1, 'stock_quantity': 153.5, 'last_update': '2025-05-11', 'product': {'unit': 'Kg', 'price': 0.0, 'tolerance': 0.2, 'product_id': 1, 'last_update': '2025-05-10', 'product_name': 'Rice', 'stock_quantity': 896}, 'distribute_quantity': 1.0}
    ]
    return render(request, 'weighting.html', {'products': products})

