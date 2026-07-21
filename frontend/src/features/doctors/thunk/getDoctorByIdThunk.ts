import { getErrorMessage } from "@/features/errors/getError";
import { doctorsService } from "@/services/doctorService";

import { createAsyncThunk } from "@reduxjs/toolkit";


export const getDoctorByIdThunk = createAsyncThunk(
  "doctor/getById",
  async (id: string, thunkApi) => {
    try {
    return await doctorsService.getDoctorProfile(id)
    }
    catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e))
      
   }
  }
);