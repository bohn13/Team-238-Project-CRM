import { useEffect, useState } from "react";
import { Input } from "../input/Input";
import { useDebounce } from "@/hooks/useDebounce"
type Props = {
   className?: string;
  search: string;
  specialization: string;
  employmentType: string;

  specializations: string[];

  onSearchChange: (value: string) => void;
  onSpecializationChange: (value: string) => void;
  onEmploymentTypeChange: (value: string) => void;
};


export const Filter: React.FC<Props> = ({ className, specialization,
employmentType,
 specializations,
  search,
  onSearchChange,
  onSpecializationChange,
onEmploymentTypeChange,
}) => {
  const [value, setValue] = useState(search);

  const debouncedSearch = useDebounce(value, 500);

  useEffect(() => {
    onSearchChange(debouncedSearch);
  }, [debouncedSearch]);

  return (
    <div className ={`flex items-center gap-2  ${className ?? ""}`} >
      <Input 
        name="124"
        type="search"
        value={value}
        placeholder="Search doctor..."
        onChange={(e) => setValue(e.target.value)}
        className="w-[250px] h-[36px] rounded-[8px]  bg-white color-[#6B7280] "
      />
       <select
        value={specialization.value}
        onChange={(e) => onSpecializationChange(e.target.value)}
        className="w-[190px] h-[36px]  rounded-[8px]  bg-white color-[#6B7280] border-1 border-[#E5E7EB]" 
      >
        <option value="">All specializations</option>

        {specializations.map((item) => (
          <option key={item.label} value={item.value}>
            {item.label}
          </option>
        ))}
      </select>

      <select
        value={employmentType}
        onChange={(e) => onEmploymentTypeChange(e.target.value)}
      className=  "w-[140px] h-[36px] rounded-[8px] bg-white color-[#6B7280] border-1 border-[#E5E7EB]"
      >
        <option value="">All types</option>
        <option value="full_time">Full time</option>
        <option value="part_time">Part time</option>
      </select>

    </div>
  );
};
      
  