import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
  className?: string;
};

export const Td = ({ children, className = "" }: Props) => {
  return (
    <td
      className={`px-6 py-4 text-sm text-gray-900 border-t border-gray-100 ${className}`}
    >
      {children}
    </td>
  );
};