import type { ThunkAction, Action } from '@reduxjs/toolkit';
import { configureStore } from '@reduxjs/toolkit';
import authReducer from '@/features/auth/authSlice'
import userReducer from "@/features/users/userSlice"
import doctorReducer from "@/features/doctors/doctorsSlice"
const store = configureStore({
  reducer: {
auth:authReducer,
    user: userReducer,  
  doctor: doctorReducer,
  },
});

export default store;

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;



export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;

