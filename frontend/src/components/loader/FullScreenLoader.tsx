import { RiToothLine } from "react-icons/ri";

export const FullScreenLoader = () => {
  return (
    <div className="fixed inset-0 z-100 flex items-center justify-center bg-white/80 backdrop-blur-sm">
      <div className="relative h-16 w-16">
     
        <div className="absolute inset-0 animate-spin rounded-full border-[5px] border-gray-300 border-t-blue-600" />

        
        <div className="absolute inset-0 flex items-center justify-center">
          <RiToothLine className="text-3xl text-blue-600" />
        </div>
      </div>
    </div>
  );
};