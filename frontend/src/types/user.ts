export type User = {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  role?: 'admin' | 'user' | 'doctor' |'superadmin'
  phoneNumber: number,
  registrationDate?: Date,
  source?: string,
  

}