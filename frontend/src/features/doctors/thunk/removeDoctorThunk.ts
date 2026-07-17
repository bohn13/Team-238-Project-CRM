import { getErrorMessage } from "@/features/errors/getError";
import { userService } from "@/services/userService";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const removeDoctorThunk = createAsyncThunk(
  "doctors/delete",
  async ({ id }: { id: string }, thunkApi) => {
    try {
      await userService.deleteDoctor(id);
      return id;
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
