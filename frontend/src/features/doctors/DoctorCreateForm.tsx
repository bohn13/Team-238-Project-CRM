import { FormProvider, useForm } from "react-hook-form";
import { ButtonPage } from "@/components/button/ButtonsPage";
import { useAppDispatch, useAppSelector } from "@/app/store/hook";

import { useEffect, useState } from "react";
import { searchUsersThunk } from "../users/searchUserThunk";
import { Search } from "@/components/search/Search";
import type { User } from "@/types/User";
import { Loader } from "@/components/loader/Loader";
import { errorToast, successToast } from "@/components/pushAppMessage/PushApp";
import type { DoctorFormData } from "@/types/dotorFormData";
import { DoctorFormFields } from "@/components/formField/DoctorFormFields";
import { createDoctorThunk } from "./thunk/createDoctorThunk";

type Props = {
  handleAside: () => void;
};

export const DoctorCreteForm: React.FC<Props> = ({ handleAside }) => {
 
  const methods = useForm<DoctorFormData>();
  const { reset, setValue, handleSubmit } = methods;

  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const dispatch = useAppDispatch();
  const { users, loading } = useAppSelector((state) => state.user);
  const { loading: doctorsLoading } = useAppSelector((state) => state.doctor);

  useEffect(() => {
    if (!selectedUser) return;

    setValue("firstName", selectedUser.firstName);
    setValue("lastName", selectedUser.lastName);
    setValue("email", selectedUser.email);
  }, [selectedUser, setValue]);

  const onSubmit = async (data: DoctorFormData) => {
    if (!selectedUser) {
      return;
    }
    try {
      await dispatch(
        createDoctorThunk({
          ...data,
          userId: selectedUser.id,
        }),
      ).unwrap();
      reset();
      successToast(
        <>
          Doctor created successfully
          <br />
          Dr. {selectedUser.firstName} {selectedUser.lastName}
        </>,
      );
    } catch (e) {
      errorToast(e as string);
    }
  };

  return (
    <>
      {" "}
      {doctorsLoading ? (
        <Loader />
      ) : (
        <div className="w-full">
          <section>
            <Search
              items={users}
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
