import { navigation } from "@/shared/config/navigation";
import type React from "react";
import { NavLink } from "react-router-dom";

export const NavBar: React.FC = () => {
  return (
    <>
      <div className=" flex flex-col w-[260px] p-[16px] h-full bottom-0 bg-[#fff]">
        <div className="flex border-b  border-[#F3F4F6]  mb-[24px] p-[16px]">
          <img className="mr-[8px]" src="smallLogo.png" alt="smallLogo" />
          <div className="flex flex-col ">
            <span className=" m-0 p-0 font-[Inter] font-semibold text-[18px]">
              {"LumiDent"}
            </span>
            <span className="m-0 p-0 leading-[16px] font-[Inter] font-medium text-[12px] text-[#6B7280]">
              {"Admin Panel"}
            </span>
          </div>
        </div>

        <nav className="flex flex-col">
          {
            <ul>
              {navigation.map((nav) => (
                <li
                  key={nav.title}
                  className=" flex justify-right w-full h-[40px] mb-[8px] "
                >
                  <NavLink className={({ isActive }) => `flex items-center h-full w-full  rounded-[8px] pl-[12px] pr-[12px]  hover:bg-[#EFF6FF] hover:text-[#1E3A8A]
                  ${isActive
                    ? "text-[#1E3A8A] bg-[#DBEAFE]"
                    : "text-[#1F2937]"}
                    `} to={nav.path}>
                    <span className="w-[20px] h-[20px] mr-[8px]">
                      {nav.icon}
                    </span>
                    <span className="font-[Inter] font-medium text-[16px] ">
                      {" "}
                      {nav.title}{" "}
                    </span>
                  </NavLink>
                </li>
              ))}
            </ul>
          }
        </nav>
        
      </div>
      
    </>
  );
};
