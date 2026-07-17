import { Rectangle } from "./component/Rectangle"


export const Logo = () => {
  return (
    <div className="  w-65.5 h-115.25 flex flex-col bg-[#111827]">
      <div className="flex flex-row">
      <div className="flex flex-col" >
         <div className="w-10 h-10 rounded-[50vw] bg-[#60A5FA] ml-9.5 mb-2.5">
       
      </div>
      <Rectangle  height="49px" width="73px" bgColor="#BEF264" ml="10px" mb="20px" radiusBL="5%" radiusBR="35%" radiusTL="35%" radiusTR="5%" rotate="5deg"/>
      <Rectangle image="./logo1.png" height="190px" width="106px" radiusTL="5%" radiusTR="35%" radiusBR="5%" radiusBL="35%" />
</div>
        <Rectangle
         image="./logo2.png" height="315px" width="140px" mb="16px" ml="16px" radiusTL="35%" radiusTR="5%" radiusBL="5%" radiusBR="35%" />
      </div>
      <Rectangle image="./logo3.png" height="130px" width="262px" radiusTL="5%" radiusTR="35%" radiusBL="35%" radiusBR="5%"/>
    </div>
  )
}