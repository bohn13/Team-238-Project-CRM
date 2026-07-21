
import { Navigate } from "react-router-dom";
import { LoginForm } from "./components/loginForm/LoginForm"
import { Logo } from "@/components/logo/Logo"
import { useAppSelector } from "@/app/store/hook";
import { Loader } from "@/components/loader/Loader";
import { Toaster } from "react-hot-toast";
import { FullScreenLoader } from "@/components/loader/FullScreenLoader";


export const LoginPage = () => {
  const { isAuth, isInitialized , loading} = useAppSelector(state => state.auth);
  if (!isInitialized) {
  return <FullScreenLoader/>;
}

if (isAuth) {
  return <Navigate to="/dashboard" replace />;
}


  return (<> <div className="flex flex-row h-screen w-screen bg-amber-800"  >
      <div className="flex flex-col justify-center items-center w-1/2 h-full bg-[#111827]">
        <Logo/>
      </div>
      <div className="flex flex-col justify-center items-center w-1/2 bg-white">
      {loading ? <Loader /> : <LoginForm />} 
      <Toaster  position="bottom-right"
  reverseOrder={false}/>
      </div>
  </div>
  </>
   
  )
}