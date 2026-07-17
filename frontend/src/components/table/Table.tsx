import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

export const Table = ({ children }: Props) => {
  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
      <table className="w-full border-collapse">
        {children}
      </table>
    </div>
  );
};