
import { createAsyncThunk } from "@reduxjs/toolkit";

import type { DoctorFormData } from "@/types/dotorFormData";
import { getErrorMessage } from "@/features/errors/getError";
import { doctorsService } from "@/services/doctorService";

export const createDoctorThunk = createAsyncThunk(
  "doctors/profile",
  async (data:DoctorFormData, thunkApi) => {
    
    try {
      await doctorsService.createDoctor(data)
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e))

    }
  }
)