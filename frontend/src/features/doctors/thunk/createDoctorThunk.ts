import { userService } from "@/services/userService";
import { createAsyncThunk } from "@reduxjs/toolkit";

import type { DoctorFormData } from "@/types/dotorFormData";
import { getErrorMessage } from "@/features/errors/getError";

export const createDoctorThunk = createAsyncThunk(
  "doctors/profile",
  async (data:DoctorFormData, thunkApi) => {
    
    try {
      await userService.createDoctor(data)
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e))

    }
  }
)