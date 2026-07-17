
import toast, { type Renderable } from "react-hot-toast";

export const successToast = (message: Renderable) => {
  toast.success(message, {
    style: {
      background: "#86EFAC",
      color: "#115E59",
    },
  });
};

export const errorToast = (message:Renderable) => {
  toast.error(message, {
    style: {
      background: "#FEE2E2",
      color: "#991B1B",
    },
  });
};