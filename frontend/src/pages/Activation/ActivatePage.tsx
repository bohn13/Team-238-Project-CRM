import { useAppDispatch } from "@/app/store/hook";
import { errorToast, successToast } from "@/components/pushAppMessage/PushApp";
import { activateAccountThunk } from "@/features/users/activationAccountThunk";
import { useEffect } from "react";
import { Toaster } from "react-hot-toast";
import { useNavigate } from "react-router-dom";


export const ActivatePage = () => {
  
const navigate = useNavigate()
 const params = new URLSearchParams(window.location.hash.split("?")[1]);

const email = params.get("email");
const token = params.get("token");
  
 
const dispatch = useAppDispatch();

useEffect(() => {
  if (!email || !token) return;

  dispatch(activateAccountThunk({ email, token }))
    .unwrap()
    .then(() => {
      successToast("Account activated");
      navigate("/login");
    })
    .catch((e) => {
      errorToast(e);
    });
}, [dispatch, email, token, navigate]);

  return <> <Toaster/></>;
};