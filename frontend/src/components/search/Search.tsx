import { useEffect, useState } from "react";
import { Input } from "@/components";
import { Loader } from "../loader/Loader";
import type { User } from "@/types/User";

type Props<T> = {
  items: T[];
  loading: boolean;
  placeholder?: string;

  onSearch: (value: T) => void;
  onSelect?: (item: T) => void;
  selectedUser: User | null;
  getKey: (item: T) => React.Key;
  renderItem: (item: T) => React.ReactNode;
  getValue: (item: T) => string;
};

export function Search<T>({
  items,
  loading,
  placeholder = "Search...",
  onSearch,
  onSelect,
  selectedUser,
  getKey,
  renderItem,
  getValue,
}: Props<T>) {
  const [query, setQuery] = useState("");
  const open = query.trim().length >= 3;

  useEffect(() => {
    if (!open) {
      return
    }
     
    const timer = setTimeout(() => {
      onSearch(query);
      
    }, 500);

    return () => clearTimeout(timer);
  }, [query]);

  return (
    <div className="relative">
      <Input
        className="border-[1px] border-[#E5E7EB] rounded-[8px]"
        name="search"
        type="search"
        placeholder={placeholder}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {open && (
        <div className="absolute left-0 right-0 top-full mt-1 max-h-60 overflow-y-auto bg-amber-50 z-30">
          {loading && (
            <div className="p-3 text-center">
              <Loader/>
            </div>
          )}

          {!loading &&
            items.map((item) => (
              <button
                key={getKey(item)}
                type="button"
                className="block w-full p-3 text-left hover:bg-[#DBEAFE]"
                onClick={() => {
                  onSelect(item);
                  setQuery(getValue(item));
               
                }}
              >
                {renderItem(item)}
              </button>
            ))}

          {!loading && items.length === 0 && !selectedUser&& (
            <div className="p-3 text-center text-gray-500">
              Nothing found
            </div>
          )}
        </div>
      )}
    </div>
  );
}