import { FormProvider, useForm } from "react-hook-form";
import { ButtonPage } from "@/components/button/ButtonsPage";
import { useAppDispatch, useAppSelector } from "@/app/store/hook";
import { Loader } from "@/components/loader/Loader";
import { errorToast, successToast } from "@/components/pushAppMessage/PushApp";
import type { DoctorFormData } from "@/types/dotorFormData";
import { DoctorFormFields } from "@/components/formField/DoctorFormFields";
import { setSelectedDoctor } from "./doctorsSlice";

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

  console.log(selectedDoctor);
  useEffect(() => {
    if (!selectedDoctor) return;

    reset({
      firstName: selectedDoctor.firstName,
      lastName: selectedDoctor.lastName,
      email: selectedDoctor.email,
      phone: selectedDoctor.phoneNumber,
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
    try {
      await dispatch(updateDoctorThunk({ id: doctorId, data })).unwrap();
      reset();
      successToast(
        <>
          Doctor updates successfully
          <br />
          Dr. {setSelectedDoctor.firstName} {setSelectedDoctor.lastName}
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
              <DoctorFormFields />

              <div className="flex w-full gap-4 border-t border-[#D1D5DB]">
                <ButtonPage className="flex-1" onClick={handleAside}>
                  Cancel
                </ButtonPage>

                <ButtonPage type="submit" className="flex-1">
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
