import { getErrorMessage } from "@/features/errors/getError";
import { patientsService } from "@/services/patientService";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const getAllPatientThunk = createAsyncThunk(
  "patients",
  async (_, thunkApi) => {
    try {
      return await patientsService.getAllPatients()
    }
    catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e))
    }
  }
)