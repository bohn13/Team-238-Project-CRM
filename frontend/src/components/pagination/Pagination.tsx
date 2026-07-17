type Props = {
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
};

export const Pagination: React.FC<Props> = ({
  page,
  pageSize,
  total,
  onPageChange,
}) => {
  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="flex items-center justify-between mt-6">
      <p className="text-sm text-gray-500">
        Showing {(page - 1) * pageSize + 1}-
        {Math.min(page * pageSize, total)} of {total}
      </p>

      <div className="flex gap-2">
        <button
          disabled={page === 1}
          onClick={() => onPageChange(page - 1)}
          className="rounded-[8px] color-[#1F2937] cursor-pointer disabled:opacity-50"
        >
          {"< Previous"}
        </button>

        {Array.from({ length: totalPages }).map((_, index) => (
          <button
            key={index}
            onClick={() => onPageChange(index + 1)}
            className={` w-[38px] h-[38px]  rounded -[8px] cursor-pointer ${
              page === index + 1
                ? "bg-[#DBEAFE] text-[blue]"
                : ""
            }`}
          >
            {index + 1}
          </button>
        ))}

        <button
          disabled={page === totalPages}
          onClick={() => onPageChange(page + 1)}
          className="rounded-[8px] color-[#1F2937] cursor-pointer disabled:opacity-50"
        >
          {" Next >"}
        </button>
      </div>
    </div>
  );
};