
import { Navigate, Outlet } from "react-router-dom";
import { useAppSelector } from "@/app/store/hook";

export const ProtectedRoute = () => {
  const auth = useAppSelector(
    state => state.auth
  );

  if (!auth.isInitialized) {
    return ('user not found')
  }

  if (!auth.isAuth) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet/>
}