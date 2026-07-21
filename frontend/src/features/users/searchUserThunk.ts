import { userService } from "@/services/userService";
import { createAsyncThunk } from "@reduxjs/toolkit";
import { getErrorMessage } from "../errors/getError";
import type { User } from "@/types/User";

export const searchUsersThunk = createAsyncThunk<User[],string | undefined>(
  "accounts/users",
  async (search, thunkAPI) => {
    try {
      return await userService.getAllUsers(search);
    } catch (error) {
      return thunkAPI.rejectWithValue(getErrorMessage(error));
    }
  },
);
