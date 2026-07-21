import { useAppDispatch, useAppSelector } from "@/app/store/hook";
import { AsideMenu } from "@/components/asideMenu/AsideMenu";
import { ButtonPage } from "@/components/button/ButtonsPage";
import { Filter } from "@/components/filter/Filter";
import { Loader } from "@/components/loader/Loader";
import { PageTitle } from "@/components/pageTitle/PageTitle";
import { Pagination } from "@/components/pagination/Pagination";
import { Sort } from "@/components/sorter/Sort";
import { Table } from "@/components/table/Table";
import { Td } from "@/components/table/Td";
import { Th } from "@/components/table/Th";
import { UserContacts } from "@/components/userContacts/UserContacts";
import { DoctorCreteForm } from "@/features/doctors/DoctorCreateForm";
import { setQuery } from "@/features/doctors/doctorsSlice";
import { specializations } from "@/features/doctors/model/specialties";
import { getAllDoctorsThunk } from "@/features/doctors/thunk/getAllDoctorsThunk";
import { useEffect, useState } from "react";
import { BiPlus } from "react-icons/bi";
import { useNavigate } from "react-router-dom";

export const DoctorsPage = () => {
  const [aside, setOpenAside] = useState(false);
  const { doctors, total, loading, query } = useAppSelector(
    (state) => state.doctor,
  );
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        await dispatch(getAllDoctorsThunk(query)).unwrap();
      } catch (error) {
        console.error(error);
      }
    };

    fetchDoctors();
  }, [dispatch, query]);
  

  const handleAside = () => setOpenAside((prev) => !prev);
  return (
    <>
      {aside && (
        <AsideMenu
          handleAside={handleAside}
          forms={<DoctorCreteForm handleAside={handleAside} />}
          title={"ADD NEW DOCTOR"}
          description={"Fill in the details below"}
        />
      )}

      <div className="flex justify-between items-center  mb-[26px] h-[57px]">
        <PageTitle
          text={`All doctors`}
          description={`showing ${total} doctors`}
        />
        <div className="flex  gap-4  ">
          <ButtonPage
            className="pl-[12px] pr-[12px] "
            onClick={handleAside}
            icon={<BiPlus className="mr-[8px]" />}
          >
            Add doctor
          </ButtonPage>
        </div>
      </div>

      <div className="flex  justify-between">
        <Filter
          className="mb-[24px]"
          search={query.search}
          specialization={query.specialization}
          employmentType={query.employmentType}
          specializations={specializations}
          onSearchChange={(value) =>
            dispatch(setQuery({ search: value, page: 1 }))
          }
          onSpecializationChange={(value) =>
            dispatch(setQuery({ specialization: value, page: 1 }))
          }
          onEmploymentTypeChange={(value) =>
            dispatch(setQuery({ employmentType: value, page: 1 }))
          }
        />
        <Sort
          sortBy={query.sortBy}
          sortOrder={query.sortOrder}
          onChange={(sortBy, sortOrder) =>
            dispatch(
              setQuery({
                sortBy,
                sortOrder,
                page: 1,
              }),
            )
          }
        />
      </div>

      {loading ? (
        <Loader />
      ) : (
        <div className="w-full p-[24p]">
          <Table>
            <thead>
              <tr>
                <Th>ID</Th>
                <Th>DOCTOR/CONTACT</Th>
                <Th>WORKLOAD</Th>
                <Th>SPECIALITY</Th>
                <Th>SCHEDULE</Th>
                <Th>TYPE</Th>
              </tr>
            </thead>
            <tbody>
              {doctors.map((doctor) => (
                <tr
                  key={doctor.id}
                  onClick={() => {
                    navigate(`/doctors/${doctor.id}`);
                  }}
                  className=" h-[76px] cursor-pointer hover:bg-[#DCFCE7] transition-colors"
                >
                  <Td>{`#${doctor.doctorCode}`}</Td>

                  <Td>
                    <UserContacts
                      avatar = {doctor.avatarUrl}
                      firstName={doctor.firstName}
                      lastName={doctor.lastName}
                      phone={doctor.phoneNumber}
                    />
                  </Td>

                  <Td>{doctor.email}</Td>

                  <Td>{doctor.specialization}</Td>

                  <Td>{"09:00-18:00"}</Td>

                  <Td>{doctor.employmentType}</Td>
                </tr>
              ))}
             
              </tbody>
              
            </Table>
             {doctors.length === 0 && (
                <p className="p-3 text-center text-gray-500">
                  Nothing found
                </p>
              )}
        </div>
      )}

      <Pagination
        page={query.page}
        pageSize={query.pageSize}
        total={total}
        onPageChange={(page) =>
          dispatch(
            setQuery({
              page,
            }),
          )
        }
      />
    </>
  );
};
