  export interface DoctorFormData {
    userId: number;
    firstName: string;
    lastName: string;
    email: string;
    phoneNumber: number;
    yearsExperience: number;
    specialization: string;
    employmentType: string;
    workingDays: string[];
    avatar?: FileList;
  };