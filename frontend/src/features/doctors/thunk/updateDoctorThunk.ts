
import { createAsyncThunk } from "@reduxjs/toolkit";
import { getErrorMessage } from "@/features/errors/getError";
import { doctorsService } from "@/services/doctorService";
import type { Doctor } from "@/types/doctor";

interface UpdateDoctorPayload {
  id: string;
  data: FormData;
}
export const updateDoctorThunk = createAsyncThunk<
  Doctor,
  UpdateDoctorPayload
>(
  `doctors/profile`,
  async ({ id, data }, thunkApi) => {
    try {
      return await doctorsService.updateDoctor(data, id);
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
