import { useAppDispatch, useAppSelector } from "@/app/store/hook";
import { logoutThunk } from "@/features/auth/logOutThunk";
import { CiLogout } from "react-icons/ci";
import { errorToast, successToast } from "../pushAppMessage/PushApp";
import { useState } from "react";
import { ConfirmModal } from "../confirmModal/ConfirmModal";
export const Footer: React.FC = () => {
  const [modal, setOpenModal] = useState(false);

  const dispatch = useAppDispatch();
  const {loading} = useAppSelector(state=>state.auth)
  
  const handleLogout = async () => {
    try {
      await dispatch(logoutThunk()).unwrap() 
      successToast("Logout successfuly")
    }
    catch (e) {
      errorToast(`${e}`)
      
    }

    
  }
  return (<>
    <ConfirmModal
      isOpen={modal} 
      title={"DO YOU WANT TO LEAVE?"}
      description="the session will be completed!"
    loading={loading}
    onConfirm={ handleLogout}
    onCancel ={()=>setOpenModal(false)}/>
    
    <div className=" h-[48px] pl-[16px] pr-[16px] pb-16px border-t border-[#E5E7EB]  ">
      <button disabled={loading} onClick={()=>setOpenModal(true)}
        className=" w-full h-full 
    flex items-center  rounded-[8px]
     pl-[12px] pr-[12px] 
      hover:bg-[#EF4444]
       hover:text-[#FFFF]
   text-[#1F2937]">
        
    <>
      <CiLogout className="w-[20px] h-[20px] mr-[8px]" />
      <span>Log out</span>
    </>
  </button>
    </div></>)
}