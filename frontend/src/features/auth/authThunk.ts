import { accessTokenService } from "@/services/accessTokenService";
import { authService } from "@/services/authService";
import { refreshTokenService } from "@/services/refreshTokenService";
import { userService } from "@/services/userService";
import { createAsyncThunk } from "@reduxjs/toolkit";
import { getErrorMessage } from "../errors/getError";
import type { LoginData } from "@/types/loginFormData";

export const loginThunk = createAsyncThunk(
  "accounts/login",
  async (data: LoginData, thunkApi) => {
    try {
      const tokens = await authService.login(data);
      accessTokenService.save(tokens.accessToken);
      refreshTokenService.save(tokens.refreshToken);
      const user = await userService.getCurrentUser();

      return { ...tokens, user };
    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    }
  },
);
