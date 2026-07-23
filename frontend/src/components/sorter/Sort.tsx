import { RiArrowUpDownLine } from "react-icons/ri";
type SortBy =
  | "name"
  | "specialization"
  | "years_experience"
  | "created_at";

type SortOrder = "asc" | "desc";

type Props = {
  className?: string;
  sortBy: SortBy;
  sortOrder: SortOrder;

  onChange: (
    sortBy: SortBy,
    sortOrder: SortOrder
  ) => void;
};

const buttons: {
  value: SortBy;
  label: string;
}[] = [
  {
    value: "name",
    label: "Name",
  },
  {
    value: "specialization",
    label: "Specialization",
  },
  {
    value: "yearsExperience",
    label: "Experience",
  },
];

export const Sort: React.FC<Props> = ({className,
  sortBy,
  sortOrder,
  onChange,
}) => {
  const handleClick = (value: SortBy) => {
    if (value === sortBy) {
      onChange(
        value,
        sortOrder === "asc" ? "desc" : "asc"
      );
    } else {
      onChange(value, "asc");
    }
  };

  return (
    <div className={`h-[32px] flex  items-center gap-4 ${className ?? ""}`}>
      <div className="flex items-center justify-center gap-1">
  <RiArrowUpDownLine className="h-3 w-3" />
  <span>Sort:</span>
</div>
     
      {buttons.map((button) => (
        <button
          key={button.value}
          onClick={() => handleClick(button.value)}
          className={` h-[32px] flex items-center rounded-[8px] pl-[12px] pr-[12px] pb-[8px] pt-[8px]   transition
            ${
              sortBy === button.value
                ? "border-blue-600 bg-blue-600 text-white"
                : "border-gray-300 bg-white hover:bg-[#DBEAFE]"
            }`}
        >
          {button.label}

          {sortBy === button.value && (
            <span className="ml-2">
              {sortOrder === "asc" ? "↑" : "↓"}
            </span>
          )}
        </button>
      ))}
    </div>
  );
};