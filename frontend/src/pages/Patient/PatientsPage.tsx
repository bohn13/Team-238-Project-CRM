import { ButtonPage } from "@/components/button/ButtonsPage";
import { PageTitle } from "@/components/pageTitle/PageTitle";
import { useState } from "react";
import { BiPlus } from "react-icons/bi";

export const PatientsPage = () => {
    const [aside, setOpenAside] = useState(false)
    const handleAside = () =>
        setOpenAside(prev=>!prev)
    return  <div className="flex justify-between items-center  mb-[26px] h-[57px]" >
          <PageTitle
          text={`All patients`}
            description={'12 die'} />
          <div className="flex  gap-4  ">
         
            <ButtonPage className="pl-[12px] pr-[12px]"
               onClick={handleAside}
              
              icon={<BiPlus className="mr-[8px]" />} >Add patients</ButtonPage>
          </div>
         
        </div>;
};
