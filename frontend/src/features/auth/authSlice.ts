import { createSlice} from "@reduxjs/toolkit";
import { loginThunk } from "./authThunk";
import { refreshThunk } from "./refreshThunk";
import { logoutThunk } from "./logOutThunk";
import type { User } from "@/types/User";

interface authState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuth: boolean;
  loading: boolean;
  isInitialized: boolean;
  error: null | string;
}

const initialState: authState = {
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuth: false,
  loading: false,
  error: null,
  isInitialized:false,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
  }, extraReducers: (builder) => {
    builder
      .addCase(loginThunk.pending, state => {
        state.loading = true;
      
      })
      .addCase(loginThunk.fulfilled, (state, action) => {
        state.accessToken = action.payload.accessToken;
        state.refreshToken = action.payload.refreshToken;
        state.user = action.payload.user;
        state.isAuth = true;
       
        state.loading = false;
      })
      .addCase(loginThunk.rejected, (state) => {
        state.user = null;
        state.accessToken = null;
        state.refreshToken = null;
        state.isAuth = false;
        state.isInitialized = true;
        state.loading = false;
      })
      .addCase(refreshThunk.fulfilled, (state, action) => {
       state.accessToken = action.payload.accessToken
        state.user = action.payload.user;
        state.isAuth = true;
        state.isInitialized = true;
        state.loading = false;
      })
      .addCase(refreshThunk.rejected,(state)=> {
    state.user = null;
        state.accessToken = null;
        state.refreshToken = null;
        state.isAuth = false;
        state.isInitialized = true;
      })
      .addCase(logoutThunk.pending, state => {
        state.loading = true;
      })
      .addCase(logoutThunk.fulfilled, (state) => {
        state.accessToken = null;
        state.refreshToken = null;
        state.isAuth = false;
        state.user = null;
        state.loading = false;
        
        
      })
      .addCase(logoutThunk.rejected, (state) => {
          state.user = null;
        state.accessToken = null;
        state.refreshToken = null;
        state.isAuth = false;
        state.loading = false;
        
      
    })
  }
});

export const {} = authSlice.actions;
export default authSlice.reducer;
