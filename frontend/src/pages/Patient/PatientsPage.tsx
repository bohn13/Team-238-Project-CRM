import { useAppDispatch, useAppSelector } from "@/app/store/hook";
import { AsideMenu } from "@/components/asideMenu/AsideMenu";
import { ButtonPage } from "@/components/button/ButtonsPage";
import { Loader } from "@/components/loader/Loader";
import { PageTitle } from "@/components/pageTitle/PageTitle";
import { Table } from "@/components/table/Table";
import { PatientCreateForm } from "@/features/patients/PatientCreateForm";
import { useEffect, useState } from "react";
import { BiPlus } from "react-icons/bi";
import { Td } from "@/components/table/Td";
import { Th } from "@/components/table/Th";
import { useNavigate } from "react-router-dom";
import { UserContacts } from "@/components/userContacts/UserContacts";
import { getAllPatientThunk } from "@/features/patients/thunk/getAllPacientThunk";
export const PatientsPage = () => {
  const [aside, setOpenAside] = useState(false)
  const { loading , patients} = useAppSelector(state => state.patient)
  const dispatch = useAppDispatch();
  const navigate = useNavigate()
    const handleAside = () =>
    setOpenAside(prev => !prev)
  
  useEffect(() => {
    const fetchPatient = async () => {
      try {
        await dispatch(getAllPatientThunk())
      } 
      catch (e) {
        console.log(e)
      }
    }
    fetchPatient()
  },[dispatch])
  console.log(patients)
  return <>
    {aside && (<AsideMenu
      handleAside={handleAside}
      forms={<PatientCreateForm handleAside={handleAside}/>}
      title={"ADD NEW PATIENT"}
       description={"Fill in the details below"}
    />)}
    <div className="flex justify-between items-center  mb-[26px] h-[57px]" >
          <PageTitle
          text={`Patient Managment`}
            description={'12 die'} />
          <div className="flex  gap-4  ">
         
            <ButtonPage className="pl-[12px] pr-[12px] "
               onClick={handleAside}
              
              icon={<BiPlus className="mr-[8px]" />} >Add patients</ButtonPage>
          </div>
         
    </div>
   {loading ? (
          <Loader />
        ) : (
          <div className="w-full p-[24p]">
            <Table>
              <thead>
                <tr>
                  <Th>ID</Th>
                  <Th>PATIENT/CONTACT</Th>
                  <Th>LAST VISIT</Th>
                  <Th>TYPE OF TREATMENT</Th>
                  <Th>TOTAL VISITS</Th>
                <Th>STATUS</Th>
                <Th>ACTION</Th>
                </tr>
              </thead>
              <tbody>
                {patients.map((patient) => (
                  <tr
                    key={patient.userId}
                    onClick={() => {
                      navigate(`/patients/${patient.userId}`);
                    }}
                    className=" h-[76px] cursor-pointer hover:bg-[#DCFCE7] transition-colors"
                  >
                    <Td>{`#${patient.userId}`}</Td>
  
                    <Td>
                      <UserContacts
                        
                        firstName={patient.firstName}
                        lastName={patient.lastName}
                        phone={patient.phoneNumber}
                      />
                    </Td>
  
                    <Td>{patient.email}</Td>
  
                    <Td>{patient.gender}</Td>
  
                    <Td>{"09:00-18:00"}</Td>
  
                    <Td>{patient.address}</Td>
                  </tr>
                ))}
               
                </tbody>
                
              </Table>
               {patients.length === 0 && (
                  <p className="p-3 text-center text-gray-500">
                    Nothing found
                  </p>
                )}
          </div>
        )}</>
};
