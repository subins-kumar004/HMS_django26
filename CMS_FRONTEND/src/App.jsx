import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/Login';
import Layout from './components/layout/Layout';

// Admin Pages
import AdminDashboard from './pages/admin/Dashboard';
import AdminStaff from './pages/admin/Staff';
import AdminDoctors from './pages/admin/Doctors';
import AdminSpecializations from './pages/admin/Specializations';

import ReceptionistDashboard from './pages/receptionist/Dashboard';
import DoctorDashboard from './pages/doctor/Dashboard';
import PharmacistDashboard from './pages/pharmacist/Dashboard';
import LabtechDashboard from './pages/labtech/Dashboard';

import api from './services/api';

import GenericCRUD from './components/common/GenericCRUD';


// Field Schemas
const patientFields = [
  { name: 'patient_name', label: 'Patient Name', type: 'text' },
  { name: 'contact', label: 'Contact Number', type: 'text' },
  { name: 'age', label: 'Age', type: 'number' },
  { name: 'gender', label: 'Gender', type: 'text' },
  { name: 'address', label: 'Address', type: 'text' },
  { name: 'membership', label: 'Has Membership', type: 'checkbox' }
];

const appointmentFields = [
  { name: 'patient', label: 'Patient ID', type: 'number' },
  { name: 'doctor', label: 'Doctor ID', type: 'number' },
  { name: 'appointment_date', label: 'Date', type: 'date' },
  { name: 'appointment_time', label: 'Time', type: 'time' },
  { name: 'status', label: 'Status', type: 'select', options: [
    { value: 'Scheduled', label: 'Scheduled' },
    { value: 'Completed', label: 'Completed' },
    { value: 'Cancelled', label: 'Cancelled' }
  ]}
];

const consultationFields = [
  { name: 'appointment', label: 'Appointment ID', type: 'number' },
  { name: 'symptoms', label: 'Symptoms', type: 'textarea' },
  { name: 'diagnosis', label: 'Diagnosis', type: 'textarea' },
  { name: 'notes', label: 'Additional Notes', type: 'textarea', required: false }
];

const prescriptionFields = [
  { name: 'appointment', label: 'Appointment ID', type: 'number' },
  { name: 'medicine', label: 'Medicine ID', type: 'number' },
  { name: 'dosage', label: 'Dosage (e.g. 500mg)', type: 'text' },
  { name: 'frequency', label: 'Frequency (e.g. 1-0-1)', type: 'text' },
  { name: 'duration', label: 'Duration (e.g. 5 days)', type: 'text' }
];

const medicineFields = [
  { name: 'medicine_name', label: 'Medicine Name', type: 'text' },
  { name: 'category', label: 'Category', type: 'text' },
  { name: 'manufacturing_date', label: 'Mfg Date', type: 'date' },
  { name: 'expiry_date', label: 'Expiry Date', type: 'date' },
  { name: 'unit', label: 'Unit (Tablet/Syrup/etc)', type: 'text' },
  { name: 'status', label: 'Active Status', type: 'checkbox' }
];

const inventoryFields = [
  { name: 'medicine', label: 'Medicine ID', type: 'number' },
  { name: 'quantity', label: 'Quantity', type: 'number' },
  { name: 'reorder_level', label: 'Reorder Level', type: 'number' }
];

const labTestFields = [
  { name: 'test_name', label: 'Test Name', type: 'text' },
  { name: 'category', label: 'Category', type: 'text' },
  { name: 'amount', label: 'Cost/Amount', type: 'number' },
  { name: 'reference_range', label: 'Reference Range', type: 'text' },
  { name: 'sample_type', label: 'Sample Type', type: 'text' },
  { name: 'status', label: 'Active', type: 'checkbox' }
];

const labResultFields = [
  { name: 'appointment', label: 'Appointment ID', type: 'number' },
  { name: 'lab_test', label: 'Lab Test ID', type: 'number' },
  { name: 'instructions', label: 'Instructions', type: 'textarea', required: false },
  { name: 'test_value', label: 'Result Value', type: 'text', required: false },
  { name: 'remarks', label: 'Remarks', type: 'textarea', required: false },
  { name: 'is_active', label: 'Active', type: 'checkbox' }
];

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Navigate to="/login" replace />} />

          {/* Admin Routes */}
          <Route element={<Layout allowedRoles={['admin']} title="Admin Dashboard" />}>
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/staff" element={<AdminStaff />} />
            <Route path="/admin/doctors" element={<AdminDoctors />} />
            <Route path="/admin/specializations" element={<AdminSpecializations />} />
          </Route>

          {/* Receptionist Routes */}
          <Route element={<Layout allowedRoles={['receptionist']} title="Receptionist Dashboard" />}>
            <Route path="/receptionist" element={<ReceptionistDashboard />} />
            <Route path="/receptionist/patients" element={<GenericCRUD title="Patients" endpoint="receptionist/patients" fields={patientFields} />} />
            <Route path="/receptionist/appointments" element={<GenericCRUD title="Appointments" endpoint="receptionist/appointments" fields={appointmentFields} />} />
            <Route path="/receptionist/billing" element={<GenericCRUD title="Billing" endpoint="receptionist/billing" fields={[]} />} />
          </Route>

          {/* Doctor Routes */}
          <Route element={<Layout allowedRoles={['doctor']} title="Doctor Dashboard" />}>
            <Route path="/doctor" element={<DoctorDashboard />} />
            <Route path="/doctor/consultations" element={<GenericCRUD title="Consultations" endpoints={{ list: 'doctor/consultation/list/', create: 'doctor/consultation/create/', update: 'doctor/consultation/update/:id/' }} fields={consultationFields} />} />
            <Route path="/doctor/prescriptions" element={<GenericCRUD title="Prescriptions" endpoints={{ list: 'doctor/medicine/list/', create: 'doctor/medicine/create/', update: 'doctor/medicine/update/:id/' }} fields={prescriptionFields} />} />
          </Route>

          {/* Pharmacist Routes */}
          <Route element={<Layout allowedRoles={['pharmacist']} title="Pharmacist Dashboard" />}>
            <Route path="/pharmacist" element={<PharmacistDashboard />} />
            <Route path="/pharmacist/medicines" element={<GenericCRUD title="Medicines Catalog" endpoints={{ list: 'pharmacist/medicines', create: 'pharmacist/medicines', update: 'pharmacist/medicines/:id' }} fields={medicineFields} />} />
            <Route path="/pharmacist/inventory" element={<GenericCRUD title="Inventory" endpoints={{ list: 'pharmacist/inventory/medicine', create: 'pharmacist/inventory/medicine', update: 'pharmacist/inventory/medicine/stock/:id' }} fields={inventoryFields} />} />
          </Route>

          {/* Lab Tech Routes */}
          <Route element={<Layout allowedRoles={['lab']} title="Lab Technician Dashboard" />}>
            <Route path="/labtech" element={<LabtechDashboard />} />
            <Route path="/labtech/tests" element={<GenericCRUD title="Lab Tests" endpoints={{ list: 'labtests', create: 'labtests', update: 'labtests/:id' }} fields={labTestFields} />} />
            <Route path="/labtech/results" element={<GenericCRUD title="Test Results" endpoints={{ list: 'labtests/results', create: 'labtests/prescription/add', update: 'labtests/results/:id' }} fields={labResultFields} />} />
          </Route>

          <Route path="/unauthorized" element={<div style={{ padding: '50px', textAlign: 'center', color: 'white' }}><h1>403 - Unauthorized</h1><p>You do not have permission to view this page.</p></div>} />
          <Route path="*" element={<div style={{ padding: '50px', textAlign: 'center', color: 'white' }}><h1>404 - Not Found</h1></div>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
