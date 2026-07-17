import type { DoctorFormData } from "@/types/dotorFormData";
import { createAsyncThunk } from "@reduxjs/toolkit";

import { userService } from "@/services/userService";
import { getErrorMessage } from "@/features/errors/getError";

export const updateDoctorThunk = createAsyncThunk(
  "doctors/prodile",
  async ({ id, data }: { id: string; data: DoctorFormData }, thunkApi) => {
    try {
      return await userService.updateDoctor(id, data);
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
