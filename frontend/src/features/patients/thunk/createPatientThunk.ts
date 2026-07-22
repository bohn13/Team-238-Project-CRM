import { getErrorMessage } from "@/features/errors/getError";
import { patientsService } from "@/services/patientService";
import type { Patient } from "@/types/patient";
import type { PatientFormData } from "@/types/patientFormData";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const createPatientThunk = createAsyncThunk<Patient, PatientFormData>(
  "patients/create",
  async (data, thunApi) => {
    try {
      return await patientsService.createPatient(data);
    } catch (e) {
      return thunApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
