import { createSlice } from "@reduxjs/toolkit";
import { createUserThunk } from "./createUserThunk";
import type { User } from "@/types/User";
import { searchUsersThunk } from "./searchUserThunk";

interface userState {
  users: User[];
  selectedUser: User | null;
  loading: boolean;
  error: null | string;
}
const initialState: userState = {
  users: [],
  selectedUser: null,
  loading: false,
  error: null,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(createUserThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(createUserThunk.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(createUserThunk.rejected, (state) => {
        state.loading = false;
      })
      .addCase(searchUsersThunk.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(searchUsersThunk.fulfilled, (state, action) => {
        state.users = action.payload;
        state.loading = false;
      })
      .addCase(searchUsersThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});
export const {} = userSlice.actions;
export default userSlice.reducer;
