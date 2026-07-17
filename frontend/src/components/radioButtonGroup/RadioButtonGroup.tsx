import type {
  FieldValues,
  Path,
  RegisterOptions,
  UseFormRegister,
} from "react-hook-form";

type RadioOption = {
  label: string;
  value: string;
};

type Props<T extends FieldValues> = {
  name: Path<T>;
  label: string;
  options: RadioOption[];

  register?: UseFormRegister<T>;
  rules?: RegisterOptions<T>;

  error?: string;
};

export function RadioGroup<T extends FieldValues> ({
  name,
  label,
  options,
  register,
  rules,
  error,
}:Props<T>)  {
  return (
    <div className="flex flex-col">
      <label className="mb-[10px] font-[Inter] font-medium text-[14px]">
        {label}
      </label>

      <div className="flex gap-4">
        {options.map((option) => (
          <label
            key={option.label}
            htmlFor={`${name}-${option.label}`}
            className="flex flex-1 cursor-pointer items-center gap-2 rounded-[8px] border p-[12px] h-[44px]"
          >
            <input
              id={`${name}-${option.label}`}
              type="radio"
              value={option.value}
              {...(register ? register(name, rules) : { name })}
            />

            <span>{option.label}</span>
          </label>
        ))}
      </div>

      {error && (
        <p className="mt-2 text-[13px] text-red-500">
          {error}
        </p>
      )}
    </div>
  );
};