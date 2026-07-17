export const formValidation = {
  email: {
    required: "email is required",
    pattern: {
      value: /^\S+@\S+\.\S+$/,
      message: "email not correct!",
    },
  },

  password: {
    required: "password is required",
    pattern: {
      value:
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>_\-\\[\]\\/]).{8,}$/,
      message: "the password is wrong",
    },
  },
  phone: {
    required: "Phone number is required",
    pattern: {
      value: /^\+?[0-9]{10,15}$/,
      message: "Enter a valid phone number",
    },
  },
  name: {
    required: "First name is required",
    pattern: {
      value: /^[A-Za-zА-Яа-яІіЇїЄєҐґ]+(?:['’-][A-Za-zА-Яа-яІіЇїЄєҐґ]+)*$/,
      message: "Name can contain only letters, hyphens, and apostrophes",
    },
     },
   specialization: {
    required: "Specialization is required",
  },
    experience: {
    required: "Experience is required",
    min: {
      value: 0,
      message: "Experience cannot be negative",
    },
    max: {
      value: 60,
      message: "Experience cannot exceed 60 years",
    },
    valueAsNumber: true,
  },
workingDays: {
  validate: (value) =>
    value.length > 0 || "Select at least one working day",
},

  partTime: {
    required: "Please select employment type",
  },
}
