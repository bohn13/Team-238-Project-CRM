import { getErrorMessage } from "@/features/errors/getError";
import { doctorsService } from "@/services/doctorService";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const removeDoctorThunk = createAsyncThunk(
  "doctors/delete",
  async (id:number , thunkApi) => {
    try {
      
      await doctorsService.deleteDoctor(id);
      return id;
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
