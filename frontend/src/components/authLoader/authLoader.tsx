import { useAppDispatch, useAppSelector } from "@/app/store/hook";
import { refreshThunk } from "@/features/auth/refreshThunk";
import { useEffect } from "react";

export const AuthLoader = ({ children }) => {
  const dispatch = useAppDispatch();
  const isInitialized = useAppSelector(state=>state.auth.isInitialized)

    useEffect(() => {
  if (!isInitialized) {
    dispatch(refreshThunk());
  }
}, [dispatch, isInitialized]);

    return isInitialized? children: 'not now'
};
