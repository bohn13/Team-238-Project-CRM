import { createAsyncThunk } from "@reduxjs/toolkit";
import { userService } from "@/services/userService";
import { getErrorMessage } from "@/features/errors/getError";

export const getAllDoctorsThunk = createAsyncThunk(
  "doctors",
  async (query, thunkApi) => {
    try {
    return  await userService.getAllDoctors(query);
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
