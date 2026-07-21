
import type { User } from "@/types/User";
import { httpClient } from "../http/httpClient";
import { accessTokenService } from "./accessTokenService";
import type { UserData } from "@/types/userFormData";

export const userService = {
  getCurrentUser: async(): Promise<User> => {
    const response = await httpClient.get("accounts/users/me")
    return response.data
  },

  getAllUsers: async (search?: string): Promise<User[]> => {
    const response = await httpClient.get("accounts/users", { params: { search } })
    return response.data
  }
   ,


  register: async (data: UserData) => {
    const response =await httpClient.post("accounts/register", data, {
      headers: {
        Authorization: `Bearer ${accessTokenService.get()}`,
      },
    })
    return response.data
  },

 activation: async (email: string, token: string) => {
  const response = await httpClient.post(
    "accounts/activate",
    { email, token },
    {
      headers: {
        skipAuthInterceptor: true,
      },
    },
  );

  return response.data;
},

 
 
  
  
  }
