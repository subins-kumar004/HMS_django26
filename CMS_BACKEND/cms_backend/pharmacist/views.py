from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from administrator.models import Medicine, MedicineStock, MedicinePrescription
from .serializers import MedicineSerializer, MedicineStockSerializer


# =========================
# MEDICINE APIs
# =========================

# POST - Add Medicine
@api_view(['POST'])
def add_medicine(request):
    serializer = MedicineSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors)


# GET - List All Medicines
@api_view(['GET'])
def list_medicines(request):
    medicines = Medicine.objects.all()
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)


# GET - Medicine by ID
@api_view(['GET'])
def get_medicine(request, id):
    try:
        medicine = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        return Response({"error": "Medicine not found"})

    serializer = MedicineSerializer(medicine)
    return Response(serializer.data)


# PUT - Update Medicine
@api_view(['PUT'])
def update_medicine(request, id):
    try:
        medicine = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        return Response({"error": "Medicine not found"})

    serializer = MedicineSerializer(medicine, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# PATCH - Deactivate Medicine
@api_view(['PATCH'])
def deactivate_medicine(request, id):
    try:
        medicine = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        return Response({"error": "Medicine not found"})

    medicine.status = False
    medicine.save()

    return Response({"message": "Medicine deactivated successfully"})


# =========================
# INVENTORY APIs
# =========================

# POST - Add Inventory
@api_view(['POST'])
def add_inventory(request):
    serializer = MedicineStockSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# PUT - Update Inventory
@api_view(['PUT'])
def update_inventory(request, id):
    try:
        stock = MedicineStock.objects.get(id=id)
    except MedicineStock.DoesNotExist:
        return Response({"error": "Stock not found"})

    serializer = MedicineStockSerializer(stock, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# GET - List All Inventory
@api_view(['GET'])
def list_inventory(request):
    stock = MedicineStock.objects.all()
    serializer = MedicineStockSerializer(stock, many=True)
    return Response(serializer.data)


# GET - Inventory by Medicine
@api_view(['GET'])
def get_inventory_by_medicine(request, medicine_id):
    stock = MedicineStock.objects.filter(medicine_id=medicine_id)
    serializer = MedicineStockSerializer(stock, many=True)
    return Response(serializer.data)


# PATCH - Low Stock Check
@api_view(['PATCH'])
def flag_low_stock(request, id):
    try:
        stock = MedicineStock.objects.get(id=id)
    except MedicineStock.DoesNotExist:
        return Response({"error": "Stock not found"})

    if stock.quantity <= stock.reorder_level:
        return Response({
            "message": "Low stock alert!",
            "medicine": stock.medicine.medicine_name,
            "quantity": stock.quantity
        })
    else:
        return Response({
            "message": "Stock level is sufficient",
            "quantity": stock.quantity
        })


# =========================
# DISPENSE MEDICINE
# =========================

@api_view(['POST'])
def dispense_medicine(request):
    appointment_id = request.data.get('appointment_id')

    prescriptions = MedicinePrescription.objects.filter(appointment_id=appointment_id)

    if not prescriptions.exists():
        return Response({"error": "No prescription found for this appointment"})

    response_data = []

    for pres in prescriptions:
        medicine = pres.medicine

        try:
            stock = MedicineStock.objects.get(medicine=medicine)
        except MedicineStock.DoesNotExist:
            return Response({"error": f"Stock not available for {medicine.medicine_name}"})

        if stock.quantity <= 0:
            return Response({"error": f"{medicine.medicine_name} is out of stock"})

        stock.quantity -= 1
        stock.save()

        response_data.append({
            "medicine": medicine.medicine_name,
            "remaining_stock": stock.quantity
        })

    return Response({
        "message": "Medicines dispensed successfully",
        "details": response_data
    })