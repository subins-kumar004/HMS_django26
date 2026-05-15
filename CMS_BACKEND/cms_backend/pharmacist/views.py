from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from administrator.models import Medicine, MedicineStock, MedicinePrescription, Patient, Appointment, Bill
from .serializers import MedicineSerializer, MedicineStockSerializer, MedicinePrescriptionSerializer
from decimal import Decimal

# =========================
# MEDICINE APIs
# =========================

@api_view(['GET', 'POST'])
def manage_medicines(request):
    if request.method == 'GET':
        medicines = Medicine.objects.all()
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def medicine_detail(request, id):
    try:
        medicine = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        return Response({"error": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        serializer = MedicineSerializer(medicine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def deactivate_medicine(request, id):
    try:
        medicine = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        return Response({"error": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)

    medicine.status = False
    medicine.save()
    return Response({"message": "Medicine deactivated successfully"})


# =========================
# INVENTORY APIs
# =========================

@api_view(['GET', 'POST'])
def manage_inventory(request):
    if request.method == 'GET':
        stock = MedicineStock.objects.all()
        serializer = MedicineStockSerializer(stock, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = MedicineStockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_inventory_by_medicine(request, medicine_id):
    stock = MedicineStock.objects.filter(medicine_id=medicine_id)
    serializer = MedicineStockSerializer(stock, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_inventory_stock(request, id):
    try:
        stock = MedicineStock.objects.get(id=id)
    except MedicineStock.DoesNotExist:
        return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MedicineStockSerializer(stock, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def flag_low_stock(request, id):
    try:
        stock = MedicineStock.objects.get(id=id)
    except MedicineStock.DoesNotExist:
        return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

    if stock.quantity <= stock.reorder_level:
        return Response({
            "message": "Low stock alert!",
            "medicine": stock.medicine.medicine_name,
            "quantity": stock.quantity,
            "reorder_level": stock.reorder_level
        })
    return Response({
        "message": "Stock level is sufficient",
        "quantity": stock.quantity
    })


# =========================
# DISPENSE MEDICINE APIs
# =========================

@api_view(['GET'])
def get_patient_prescriptions(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        
    appointments = Appointment.objects.filter(patient=patient, status__in=['Scheduled', 'Completed'])
    prescriptions = MedicinePrescription.objects.filter(appointment__in=appointments).order_by('-created_at')
    
    response_data = []
    for pres in prescriptions:
        response_data.append({
            "prescription_id": pres.id,
            "appointment_id": pres.appointment.id,
            "appointment_date": pres.appointment.appointment_date,
            "medicine_id": pres.medicine.id,
            "medicine_name": pres.medicine.medicine_name,
            "dosage": pres.dosage,
            "frequency": pres.frequency,
            "duration": pres.duration,
        })
        
    return Response(response_data)

@api_view(['POST'])
def dispense_medicine(request):
    """
    Expects request.data to be like:
    {
        "appointment_id": 1,
        "dispensed_items": [
            {
                "medicine_id": 2,
                "quantity": 10,
                "cost": 50.00
            }
        ]
    }
    """
    appointment_id = request.data.get('appointment_id')
    dispensed_items = request.data.get('dispensed_items', [])

    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

    if not dispensed_items:
        return Response({"error": "No items to dispense"}, status=status.HTTP_400_BAD_REQUEST)

    response_data = []
    total_cost = Decimal('0.00')

    for item in dispensed_items:
        medicine_id = item.get('medicine_id')
        quantity = int(item.get('quantity', 0))
        cost = Decimal(str(item.get('cost', '0.00')))

        if quantity <= 0:
            return Response({"error": f"Invalid quantity for medicine ID {medicine_id}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            medicine = Medicine.objects.get(id=medicine_id)
            stock = MedicineStock.objects.get(medicine=medicine)
        except (Medicine.DoesNotExist, MedicineStock.DoesNotExist):
            return Response({"error": f"Stock not available for medicine ID {medicine_id}"}, status=status.HTTP_404_NOT_FOUND)

        if stock.quantity < quantity:
            return Response({"error": f"Insufficient stock for {medicine.medicine_name}. Available: {stock.quantity}"}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct stock
        stock.quantity -= quantity
        stock.save()

        total_cost += cost
        response_data.append({
            "medicine": medicine.medicine_name,
            "dispensed_quantity": quantity,
            "remaining_stock": stock.quantity,
            "cost": cost
        })

    # Update Bill
    try:
        bill = Bill.objects.get(appointment=appointment)
        bill.additional_charge += total_cost
        bill.total_amount = bill.consultation_fee + bill.additional_charge
        bill.save()
        bill_info = {
            "bill_id": bill.id,
            "additional_charge": str(bill.additional_charge),
            "total_amount": str(bill.total_amount)
        }
    except Bill.DoesNotExist:
        bill_info = "No bill found for this appointment"

    return Response({
        "message": "Medicines dispensed successfully",
        "details": response_data,
        "bill_updated": bill_info
    })