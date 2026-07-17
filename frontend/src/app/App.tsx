
import { Footer } from '@/components/footer/Footer';
import { Header } from '@/components/header/Header';
import { NavBar } from '@/components/navBar/NavBar';
import React from 'react';
import { Outlet } from 'react-router-dom';
import "tailwindcss";




export const App: React.FC = () => {
 
  return (<> 
    <div className='flex  h-screen' >
      <div className='flex flex-col'>
        <NavBar />
       <Footer />
      </div>
      <div className='flex-1 flex flex-col'>
        <Header /> 
        <main className="flex-1 pt-[24px] pl-[40px] pr-[40px]  overflow-auto bg-[#F3F4F6]  ">
          <Outlet/>
        </main>
      </div>
      
       
    </div>
   
  
   
    
</>
    
  );
};
