import { useEffect } from "react";
import { ButtonPage } from "../button/ButtonsPage";


type Props = {
  isOpen: boolean;

  title: React.ReactNode;
  description?: React.ReactNode;

  confirmText?: string;
  cancelText?: string;


  loading?: boolean;
  closeOnBackdrop?: boolean;

  children?: React.ReactNode;

  onConfirm: () => void | Promise<void>;
  onCancel: () => void;
};



export const ConfirmModal: React.FC<Props> = ({
  isOpen,
  loading,
  title,
  description,
  confirmText = "Confirm",
  cancelText = "Cancel",
  closeOnBackdrop = true,
  children,
  onConfirm,
  onCancel,
}) => {
  useEffect(() => {
    if (!isOpen) return;

    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onCancel();
      }
    };

    document.body.style.overflow = "hidden";

    window.addEventListener("keydown", handleEsc);

    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", handleEsc);
    };
  }, [isOpen, onCancel]);

  if (!isOpen) {
    return null;
  }

  return (<div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      onClick={() => {
        if (closeOnBackdrop) {
          onCancel();
        }
      }}
    >
      <div
        className="w-full flex flex-col items-center max-w-md rounded-xl bg-white p-6 shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="mb-2 text-[Inter] text-[30px] font-semibold ">
          {title}
        </h2>

        {description && (
          <p className="mb-6 text-gray-600">
            {description}
          </p>
        )}

        {children}

        <div className="mt-6 flex justify-end gap-3">
          <ButtonPage
            
            type="button"
            onClick={onCancel}
            disabled={loading}
            className=" w-[171px]  bg-white border"
          >
            <span className="text-[#172554]">
              {cancelText}
            </span>
          </ButtonPage>

          <ButtonPage
            type="button"
            onClick={onConfirm}
            disabled={loading}
            className={  'w-[171px] bg-[#EF4444]' }
          >
            { confirmText}
          </ButtonPage>
        </div>
      </div>
    </div>)
  
};