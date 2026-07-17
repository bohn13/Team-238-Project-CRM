import { userService } from "@/services/userService";
import { getErrorMessage } from "../errors/getError";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const activateAccountThunk = createAsyncThunk(
  "users/activate",
  async (
    { email, token }: { email: string; token: string },
    thunkAPI
  ) => {
    try {
      await userService.activation(email, token);
    } catch (e) {
      return thunkAPI.rejectWithValue(getErrorMessage(e));
    }
  }
);