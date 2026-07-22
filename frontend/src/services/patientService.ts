import { httpClient } from "@/http/httpClient";
import type { PatientFormData } from "@/types/patientFormData";
import { accessTokenService } from "./accessTokenService";


export const patientsService = {
  createPatient: async (data: PatientFormData) => {
    const response = await httpClient.post("/patients", data, {
      headers: {
        Authorization: `Bearer ${accessTokenService.get()}`,
      },
    });
    return response.data;
  },
  getAllPatients: async () => {
    const response = await httpClient.get("patients", {
       headers: {
        Authorization: `Bearer ${accessTokenService.get()}`,
      },
    })
    return response.data
  }
};
