import type { DoctorQuery } from "@/features/doctors/model/DoctorQuery";
import { httpClient } from "@/http/httpClient"
import type { DoctorFormData } from "@/types/dotorFormData";
import { accessTokenService } from "./accessTokenService";

export const doctorsService = {

   getDoctorProfile: async(id: string) => {
      const response = await httpClient.get(`doctors/${id}/profile`)
      return response.data
  },

  getAllDoctors: async(query: DoctorQuery) => {
    const params: Record<string, string | number> = {
      page: query.page,
      page_size: query.pageSize,
      sort_by: query.sortBy,
      sort_order: query.sortOrder,
    };
  
    if (query.search) {
      params.search = query.search;
    }
  
    if (query.specialization) {
      params.specialization = query.specialization;
    }
  
    if (query.employmentType) {
      params.employment_type = query.employmentType;
    }
  
    const response = await httpClient.get("doctors", { params });
    return response.data
  },

   createDoctor: async(
     data:DoctorFormData
    ) => {
      const response = await httpClient.post(
        "doctors/profile",
        data,
        {
          headers: {
            Authorization: `Bearer ${accessTokenService.get()}`,
          },
        },
     ) 
     return response.data
  },
   
  updateDoctor: async(
  id: string,
  data: DoctorFormData
) => {
  const response = await httpClient.patch(
    `doctors/${id}/profile`,
    data,
    {
      headers: {
        Authorization: `Bearer ${accessTokenService.get()}`,
      },
    }
    )
    return response.data
  },
    
  deleteDoctor: async(id: number) => {
    const response= await httpClient.delete(
      `doctors/${id}/`, {
      headers: {
        Authorization: `Bearer ${accessTokenService.get()}`,
      },
    })
    return response.data
   } 
}