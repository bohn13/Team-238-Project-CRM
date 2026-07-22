import { useAppDispatch, useAppSelector } from "@/app/store/hook";
import { errorToast, successToast } from "@/components/pushAppMessage/PushApp";
import type { PatientFormData } from "@/types/patientFormData";
import type { User } from "@/types/User";
import { useEffect, useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { searchUsersThunk } from "../users/searchUserThunk";
import { Search } from "@/components/search/Search";
import { ButtonPage } from "@/components/button/ButtonsPage";
import { createPatientThunk } from "./thunk/createPatientThunk";
import { PatientsFormFields } from "@/components/formField/PatientFormField";

type Props = {
  handleAside: () => void;
};

export const PatientCreateForm:React.FC<Props> = ({ handleAside }) => {
  
  const methods = useForm<PatientFormData>();
    const { reset, setValue, handleSubmit } = methods;
  
    const [selectedUser, setSelectedUser] = useState<User | null>(null);
    const dispatch = useAppDispatch();
    const { users, loading } = useAppSelector((state) => state.user);
   
  
    useEffect(() => {
      if (!selectedUser) return;
      setValue("firstName", selectedUser.firstName);
      setValue("lastName", selectedUser.lastName);
      setValue("email", selectedUser.email);
    }, [selectedUser, setValue]);
  
   const onSubmit = async (data: PatientFormData) => {
    if (!selectedUser) {
      return;
    }
  
    try {
      await dispatch(createPatientThunk({
        ...data,
        userId:selectedUser.id
      })).unwrap();
  
      // await dispatch(getAllDoctorsThunk(query)).unwrap();
  
      reset();
  
      successToast(
        <>
          Patient created successfully
          <br />
          Mr. {selectedUser.firstName} {selectedUser.lastName}
        </>,
      );
    } catch (e) {
      errorToast(e as string);
    }
  };
  
    return (
      <>
        {" "}
        {/* {loading? (
          <Loader />
        ) : ( */}
            <div className="w-full">
              <section>
  
              </section>
            <section className="mb-[24px]">
              <Search
                items={users}
                placeholder="Find an activated user"
                loading={loading}
                onSearch={(value) => dispatch(searchUsersThunk(value))}
                selectedUser={selectedUser}
                onSelect={setSelectedUser}
                getKey={(user) => user.id}
                getValue={(user) => `${user.firstName} ${user.lastName}`}
                renderItem={(user) => (
                  <>
                    <div>
                      {user.firstName} {user.lastName}
                    </div>
                    <div>{user.email}</div>
                  </>
                )}
              />
            </section>
           
              <FormProvider {...methods}>
              <form
                className="flex flex-col gap-6"
                onSubmit={handleSubmit(onSubmit)}
              >
                {<PatientsFormFields type={'create'}/>}
  
                <div className="flex w-full gap-4 border-t border-[#D1D5DB]">
                  <ButtonPage className="flex-1 bg-[#FFFFFF] " onClick={handleAside}>
                      <span className="text-[#172554]">Cancel</span>
                  </ButtonPage>
  
                  <ButtonPage type="submit" className="flex-1">
                    Send an invitation
                  </ButtonPage>
                </div>
              </form>
            </FormProvider>
          </div>
        {/* )}{" "} */}
      </>
    );
  };
  
