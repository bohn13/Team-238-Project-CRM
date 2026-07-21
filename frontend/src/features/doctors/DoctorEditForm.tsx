import { FormProvider, useForm } from "react-hook-form";
import { ButtonPage } from "@/components/button/ButtonsPage";
import { useAppDispatch, useAppSelector } from "@/app/store/hook";
import { Loader } from "@/components/loader/Loader";
import { errorToast, successToast } from "@/components/pushAppMessage/PushApp";
import type { DoctorFormData } from "@/types/dotorFormData";
import { DoctorFormFields } from "@/components/formField/DoctorFormFields";


import { useParams } from "react-router-dom";
import { useEffect } from "react";
import { updateDoctorThunk } from "./thunk/updateDoctorThunk";


type Props = {
  handleAside: () => void;
};

export const DoctorEditForm: React.FC<Props> = ({ handleAside }) => {
  const methods = useForm<DoctorFormData>();
  const { reset, handleSubmit } = methods;

  const dispatch = useAppDispatch();
  const { selectedDoctor, loading } = useAppSelector((state) => state.doctor);
  const { doctorId } = useParams();

  
  useEffect(() => {
    if (!selectedDoctor) return;

    reset({
      firstName: selectedDoctor.firstName,
      lastName: selectedDoctor.lastName,
      email: selectedDoctor.email,
      phoneNumber: selectedDoctor.phoneNumber,
      specialization: selectedDoctor.specialization,
      yearsExperience: selectedDoctor.yearsExperience,
      employmentType: selectedDoctor.employmentType,
      workingDays: selectedDoctor.workingDays,
    });
  }, [selectedDoctor, reset]);

  const onSubmit = async (data: DoctorFormData) => {
    if (!selectedDoctor) {
      return;
    }
    const formData = new FormData();
    
    formData.append("specialization", data.specialization);
    formData.append("first_name", data.firstName)
    formData.append("last_name", data.lastName)
  if (data.yearsExperience !== undefined) {
    formData.append(
      "years_experience",
      String(data.yearsExperience),
    );
  }

  if (data.employmentType) {
    formData.append(
      "employment_type",
      data.employmentType,
    );
  }
if (data.phoneNumber) {
    formData.append(
      "phone_number",
      String(data.phoneNumber),
  )
 
    }
//      data.workingDays.forEach((day) => {
//   formData.append("working_days", day);
// })
    
    
  if (data.avatar?.length) {
    formData.append("avatar", data.avatar[0]);
   }
  
    try {
      await dispatch(updateDoctorThunk({
        id: doctorId,
        data: formData,
      })).unwrap();
      reset();
      successToast(
        <>
          Doctor updates successfully
          <br />
          Dr. {selectedDoctor.firstName} {selectedDoctor.lastName}
        </>,
      );
    } catch (e) {
      errorToast(e as string);
    }
  };

  return (
    <>
      {" "}
      {loading ? (
        <Loader />
      ) : (
        <div className="w-full">
          <FormProvider {...methods}>
            <form
              className="flex flex-col gap-6"
              onSubmit={handleSubmit(onSubmit)}
            >
              <DoctorFormFields/>

              <div className="flex w-full gap-4  border-t border-[#D1D5DB]">
                <ButtonPage className="flex-1  bg-[#FFFFFF] " onClick={handleAside}>
                 <span className=" text-[#172554]">Cancel</span>
                </ButtonPage>

                <ButtonPage type="submit" className="flex-1 ">
                  Send an invitation
                </ButtonPage>
              </div>
            </form>
          </FormProvider>
        </div>
      )}{" "}
    </>
  );
};
