import { useFormContext } from "react-hook-form";

import { Input } from "@/components";
import { Select } from "@/components/select/Select";
import { CheckboxGroup } from "@/components/checkBoxGroup/CheskBoxGroup";
import { RadioGroup } from "@/components/radioButtonGroup/RadioButtonGroup";


import type { DoctorFormData } from "@/types/dotorFormData";
import { formValidation } from "@/features/auth/model/form.validation";
import { specializations } from "@/features/doctors/model/specialties";
import { employmentTypes } from "@/features/doctors/model/employmentTypes";
import { workingDays } from "@/features/doctors/model/workingDays";
import { UploadAvatar } from "../uploadAvatar/UploadAvatar";
type Props = {
  type?: 'create'
}

export const DoctorFormFields:React.FC<Props> = ({type}) => {
  const {
    register,
    formState: { errors },
  } = useFormContext<DoctorFormData>();

  return (
    <>
      <section>
        <UploadAvatar/>
     


        <p className="mb-6 text-xs text-[#6B7280]">
          PERSONAL INFO
        </p>

        <div className="flex gap-4 mb-6">
          <Input
            className="flex-1"
            name="firstName"
            label="First name *"
            type="text"
            placeholder="First, select a user."
            register={register}
            rules={formValidation.name}
            error={errors.firstName?.message}
            readOnly={type === "create"}
          />

          <Input
            className="flex-1"
            name="lastName"
            label="Last name *"
            type="text"
            placeholder="First, select a user."
            register={register}
            rules={formValidation.name}
            error={errors.lastName?.message}
            readOnly={type === "create"}
          />
        </div>

        <div className="flex gap-4">
          <Select
            className="flex-1"
            name="specialization"
            label="Speciality *"
            placeholder="Enter speciality"
            option={specializations}
            register={register}
            rules={formValidation.specialization}
            error={errors.specialization?.message}
          />

          <Input
            className="flex-1"
            name="yearsExperience"
            label="Experience *"
            type="number"
            placeholder="E.g. 10"
            register={register}
            rules={formValidation.experience}
            error={errors.yearsExperience?.message}
          />
        </div>
      </section>

      <RadioGroup
        name="employmentType"
        label="Type *"
        options={employmentTypes}
        register={register}
        rules={formValidation.partTime}
        error={errors.employmentType?.message}
      />

      <section>
        <p className="mb-6 text-xs text-[#6B7280]">
          CONTACT
        </p>

        <Input
          disabled
          name="email"
          label="Email *"
          type="email"
          placeholder="example@gmail.com"
          register={register}
          rules={formValidation.email}
          error={errors.email?.message}
        />
      </section>

      <section>
        <Input
          name="phoneNumber"
          label="Phone *"
          type="tel"
          placeholder="+38 (0XX) XXX-XXXX"
          register={register}
          rules={formValidation.phone}
          error={errors.phoneNumber?.message}
        />
      </section>

      <section>
        <CheckboxGroup
          name="workingDays"
          label="Working days *"
          options={workingDays}
          disabledOptions={["Sun"]}
          register={register}
          rules={formValidation.workingDays}
          error={errors.workingDays?.message}
        />

        <p className="mt-4 mb-6 text-xs text-[#6B7280]">
          Standard hours: 09:00 - 18:00
        </p>
      </section>
    </>
  );
};