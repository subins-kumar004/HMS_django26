from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import (
    LabTest,
    LabTestPrescription
)

from .serializers import (
    LabTestSerializer,
    LabTestPrescriptionSerializer
)


# =========================
# LAB TEST LIST + ADD
# =========================

@api_view(['GET', 'POST'])
def lab_tests(request):

    # =========================
    # LIST ALL LAB TESTS
    # =========================

    if request.method == 'GET':

        tests = LabTest.objects.filter(is_active=True)

        serializer = LabTestSerializer(
            tests,
            many=True
        )

        return Response(serializer.data)

    # =========================
    # ADD LAB TEST
    # =========================

    elif request.method == 'POST':

        serializer = LabTestSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================
# GET + UPDATE LAB TEST
# =========================

@api_view(['GET', 'PUT'])
def lab_test_detail(request, labTestId):

    try:

        test = LabTest.objects.get(id=labTestId)

    except LabTest.DoesNotExist:

        return Response(
            {"error": "Lab test not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # =========================
    # GET LAB TEST BY ID
    # =========================

    if request.method == 'GET':

        serializer = LabTestSerializer(test)

        return Response(serializer.data)

    # =========================
    # UPDATE LAB TEST
    # =========================

    elif request.method == 'PUT':

        serializer = LabTestSerializer(
            test,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================
# DEACTIVATE LAB TEST
# =========================

@api_view(['PATCH'])
def deactivate_lab_test(request, labTestId):

    try:

        test = LabTest.objects.get(id=labTestId)

    except LabTest.DoesNotExist:

        return Response(
            {"error": "Lab test not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    test.is_active = False

    test.save()

    return Response(
        {"message": "Lab test deactivated successfully"}
    )


# =========================
# ADD LAB TEST PRESCRIPTION
# =========================

@api_view(['POST'])
def add_lab_test_prescription(request):

    serializer = LabTestPrescriptionSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# =========================
# RECORD LAB RESULT
# =========================

@api_view(['PUT'])
def record_lab_result(request, labTestPrescriptionId):

    try:

        prescription = LabTestPrescription.objects.get(
            id=labTestPrescriptionId
        )

    except LabTestPrescription.DoesNotExist:

        return Response(
            {"error": "Prescription not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    prescription.lab_test_value = request.data.get(
        'lab_test_value'
    )

    prescription.remarks = request.data.get(
        'remarks'
    )

    prescription.save()

    serializer = LabTestPrescriptionSerializer(
        prescription
    )

    return Response(serializer.data)


# =========================
# GET RESULTS BY APPOINTMENT
# =========================

@api_view(['GET'])
def get_results_by_appointment(request, appointmentId):

    results = LabTestPrescription.objects.filter(
        appointment_id=appointmentId,
        is_active=True
    )

    serializer = LabTestPrescriptionSerializer(
        results,
        many=True
    )

    return Response(serializer.data)


# =========================
# GET RESULTS BY DATE RANGE
# =========================

@api_view(['GET'])
def get_results_by_date_range(request):

    start_date = request.GET.get('startDate')

    end_date = request.GET.get('endDate')

    results = LabTestPrescription.objects.filter(
        prescribed_date__range=[
            start_date,
            end_date
        ],
        is_active=True
    )

    serializer = LabTestPrescriptionSerializer(
        results,
        many=True
    )

    return Response(serializer.data)


# =========================
# DEACTIVATE PRESCRIPTION
# =========================

@api_view(['PATCH'])
def deactivate_lab_test_prescription(
    request,
    labTestPrescriptionId
):

    try:

        prescription = LabTestPrescription.objects.get(
            id=labTestPrescriptionId
        )

    except LabTestPrescription.DoesNotExist:

        return Response(
            {"error": "Prescription not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    prescription.is_active = False

    prescription.save()

    return Response(
        {
            "message":
            "Prescription deactivated successfully"
        }
    )