import type {
  FieldValues,
  Path,
  RegisterOptions,
  UseFormRegister,
} from "react-hook-form";

type SelectOption = {
  label: string;
  value: string;
};

type Props<T extends FieldValues> = {
  name: Path<T>;
  label: string;
  option: SelectOption[];
  placeholder: string;
  className?: string;

  register: UseFormRegister<T>;
  rules?: RegisterOptions<T>;
  error?: string;
};

export const Select = <T extends FieldValues>({
  name,
  label,
  option,
  placeholder,
  className,
  register,
  rules,
  error,
}: Props<T>) => {
  return (
    <div className={`flex flex-col ${className ?? ""}`}>
      <label htmlFor={name} className="mb-[10px] text-[14px] font-medium">
        {label}
      </label>

      <select
        id={name}
        defaultValue=""
        {...register(name, rules)}
        className="h-[44px] rounded-[5px] border border-gray-300 px-3"
      >
        <option value="" disabled>
          {placeholder}
        </option>

        {option.map((item) => (
          <option key={item.value} value={item.value}>
            {item.label}
          </option>
        ))}
      </select>

      {error && (
        <span className="mt-1 text-sm text-red-500">
          {error}
        </span>
      )}
    </div>
  );
};