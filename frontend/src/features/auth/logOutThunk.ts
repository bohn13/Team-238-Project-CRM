
import { accessTokenService } from "@/services/accessTokenService";
import { authService } from "@/services/authService";
import { refreshTokenService } from "@/services/refreshTokenService";
import { createAsyncThunk } from "@reduxjs/toolkit";
import { getErrorMessage } from "../errors/getError";

export const logoutThunk = createAsyncThunk(
  "accounts/logout",
  async (_, thunkApi) => {
    try {
      const refreshToken = refreshTokenService.get();

      if (!refreshToken) {
        return thunkApi.rejectWithValue("No refresh token");
      }

      await authService.logout(refreshToken);
      

    } catch (e) {
      return thunkApi.rejectWithValue(getErrorMessage(e));
    } finally {
      accessTokenService.remove();
      refreshTokenService.remove();
    }
  }
);