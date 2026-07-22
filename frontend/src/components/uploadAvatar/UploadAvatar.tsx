import { useEffect, useMemo } from "react";
import { useFormContext } from "react-hook-form";
import { FiUser } from "react-icons/fi";

import { ButtonPage } from "@/components/button/ButtonsPage";

export const UploadAvatar = () => {
  const { register, watch, setValue } = useFormContext();

  const avatar = watch("avatar");

  const preview = useMemo(() => {
    if (!avatar?.length) {
      return null;
    }

    return URL.createObjectURL(avatar[0]);
  }, [avatar]);

  useEffect(() => {
    return () => {
      if (preview) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  return (
    <div className="mb-[24px] flex">
      <label
        htmlFor="avatar"
        className="flex cursor-pointer items-center"
      >
        <div className="mr-[15px] flex h-[80px] w-[80px] items-center justify-center overflow-hidden rounded-full bg-[#E5E7EB]">
          {preview ? (
            <img
              src={preview}
              alt="Doctor avatar"
              className="h-full w-full object-cover"
            />
          ) : (
            <FiUser className="h-[24px] w-[24px] text-gray-500" />
          )}
        </div>

        <div className="flex flex-col">
          <h2 className="text-[14px] font-medium text-[#2563EB]">
            Upload Photo
          </h2>

          <p className="text-[12px] text-[#9CA3AF]">
            An image of the person — best if it has the same light and height.
          </p>
        </div>
      </label>

      <input
        id="avatar"
        type="file"
        accept="image/png,image/jpeg,image/webp"
        className="hidden"
        {...register("avatar")}
      />

      {preview && (
        <ButtonPage
          type="button"
          className="ml-3 h-[24px] w-[24px] rounded-full bg-"
          onClick={() => {
            setValue("avatar", undefined, {
              shouldDirty: true,
              shouldValidate: true,
            });
          }}
        >
          ✕
        </ButtonPage>
      )}
    </div>
  );
};