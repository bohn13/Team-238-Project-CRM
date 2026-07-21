
import { createAsyncThunk } from "@reduxjs/toolkit";

import { getErrorMessage } from "@/features/errors/getError";
import { doctorsService } from "@/services/doctorService";
import type { Doctor } from "@/types/doctor";

export const createDoctorThunk = createAsyncThunk<Doctor, FormData>(
  "doctors/profiles",
  async (data, thunkApi) => {
    
    try {
  
     return await doctorsService.createDoctor(data)
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e))

    }
  }
)