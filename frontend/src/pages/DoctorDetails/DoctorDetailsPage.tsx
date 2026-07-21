import { useAppDispatch, useAppSelector } from "@/app/store/hook";
import { ButtonPage } from "@/components/button/ButtonsPage";
import { TfiPencil } from "react-icons/tfi";
import { IoTrash } from "react-icons/io5";
import { useEffect, useState } from "react";
import { AsideMenu } from "@/components/asideMenu/AsideMenu";
import { DoctorEditForm } from "@/features/doctors/DoctorEditForm";
import { useNavigate, useParams } from "react-router-dom";

import { DoctorsProfile } from "./components/DoctorsProfile";
import { getDoctorByIdThunk } from "@/features/doctors/thunk/getDoctorByIdThunk";
import { removeDoctorThunk } from "@/features/doctors/thunk/removeDoctorThunk";
import { errorToast, successToast } from "@/components/pushAppMessage/PushApp";
import { Loader } from "@/components/loader/Loader";

export const DoctorDetailsPage = () => {
  const dispatch = useAppDispatch();
  const [aside, setOpenAside] = useState(false);

  const { doctorId } = useParams();
  const navigate = useNavigate();
  const { selectedDoctor, loading } = useAppSelector((state) => state.doctor);

  useEffect(() => {
    if (!doctorId) return;

    dispatch(getDoctorByIdThunk(doctorId));
  }, [dispatch,doctorId]);


  const handleAside = () => setOpenAside((prev) => !prev);
  
  
  const handleRemove = async () => {
    
    try {
      await dispatch(removeDoctorThunk(Number(doctorId))).unwrap();
      successToast('Doctor remove')
      navigate("/doctors");
    } catch (e) {
      errorToast(e as string)
    }
    
  }

  return (
    <>
      {aside && (
        <AsideMenu
          handleAside={handleAside}
          forms={<DoctorEditForm handleAside={handleAside} />}
          title={"EDIT DOCTOR"}
          description={"Fill in the details below"}
        />
      )}

      {loading? <Loader/>: <div className="rounded-xl bg-white p-6 shadow-sm">
        <section className="mb-8 flex items-center justify-between">
          <div className="text-sm text-gray-500">
            <span className="cursor-pointer hover:text-blue-600" onClick={()=>navigate('/doctors')}>
              &lt; Doctors
            </span>

            <span className="mx-2">/</span>

            <span className="font-medium text-gray-900">
              Dr. {selectedDoctor?.firstName} {selectedDoctor?.lastName}
            </span>
          </div>

          <div className="flex gap-3">
            <ButtonPage
            
              className="bg-[#EF4444] px-4 hover:bg-black"
              icon={<IoTrash className="mr-2 text-white" />}
              onClick={ handleRemove}
            >
              Remove doctor
            </ButtonPage>

            <ButtonPage
              className="px-4"
              icon={<TfiPencil className="mr-2" />}
              onClick={handleAside}
            >
              Edit doctor
            </ButtonPage>
          </div>
        </section>

        <section className="flex items-center justify-between rounded-xl border border-gray-200 p-6">
          {!loading && selectedDoctor && (
            <DoctorsProfile selectedDoctor={selectedDoctor} />
          )}
        </section>
      </div>}
    </>
  );
};
