import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
  className?: string;
};

export const Th = ({ children, className = "" }: Props) => {
  return (
    <th
      className={`px-6 py-4 text-left text-sm font-semibold text-gray-500 ${className}`}
    >
      {children}
    </th>
  );
};