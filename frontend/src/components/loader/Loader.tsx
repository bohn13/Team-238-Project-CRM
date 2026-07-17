import { RiToothLine } from "react-icons/ri";

export const Loader = () => {
  return (
    <div className=" w-full h-full flex items-center justify-center">
      <div className="relative h-[30px] w-[30px]">
        <div className="absolute inset-0 animate-spin rounded-full border-[3px] border-gray-300 border-t-blue-600" />

        <div className="absolute inset-0 flex items-center justify-center">
          <RiToothLine className=" w-[25px] h-[25px] text-sm text-blue-600" />
        </div>
      </div>
    </div>
  );
};