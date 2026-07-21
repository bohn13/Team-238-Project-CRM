import type { DoctorFormData } from "@/types/dotorFormData";
import { createAsyncThunk } from "@reduxjs/toolkit";
import { getErrorMessage } from "@/features/errors/getError";
import { doctorsService } from "@/services/doctorService";

export const updateDoctorThunk = createAsyncThunk(
  "doctors/prodile",
  async ({ id, data }: { id: string; data: DoctorFormData }, thunkApi) => {
    try {
      return await doctorsService.updateDoctor(id, data);
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
