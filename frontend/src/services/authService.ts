import { authClient as client } from "@/http/authClient";
import { accessTokenService } from "./accessTokenService";
import type { LoginData } from "@/types/loginFormData";
import type { User } from "@/types/User";


interface AuthData {
  accessToken: string;
  refreshToken: string;
  user?:User;
}

export const authService = {
  login: async(data: LoginData): Promise<AuthData> => {
    const response = await client.post("accounts/login", data);
    return response.data
  },

  logout: async(refreshToken: string) => {
    const response = await client.post(
      "accounts/logout",
      { refreshToken },
      {
        headers: {
          Authorization: `Bearer ${accessTokenService.get()}`,
        },
      },
    );
    return response.data
  },
  refresh: async (refreshToken: string): Promise<AuthData> => {
    const response = await client.post("accounts/refresh", { refreshToken })
  return response.data}
};
