import { userService } from "@/services/userService";
import { createAsyncThunk } from "@reduxjs/toolkit";

import { getErrorMessage } from "../errors/getError";
import type { UserData } from "@/types/userFormData";

export const createUserThunk = createAsyncThunk(
  "accounts/register",
  async (data: UserData, thunkApi) => {
    try {
      await userService.register(data);
      await new Promise((resolve) => setTimeout(resolve, 3000));
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
