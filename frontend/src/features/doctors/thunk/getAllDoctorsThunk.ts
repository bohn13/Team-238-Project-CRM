import { createAsyncThunk } from "@reduxjs/toolkit";
import { getErrorMessage } from "@/features/errors/getError";
import { doctorsService } from "@/services/doctorService";
import type { DoctorQuery } from "../model/DoctorQuery";

export const getAllDoctorsThunk = createAsyncThunk(
  "doctors",
  async (query:DoctorQuery, thunkApi) => {
    try {
    return  await doctorsService.getAllDoctors(query);
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
