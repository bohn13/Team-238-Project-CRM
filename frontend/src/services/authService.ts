import { authClient as client } from "@/http/authClient";
import { accessTokenService } from "./accessTokenService";
import type { LoginData } from "@/types/loginFormData";

interface AuthData {
  accessToken?: string;
  refreshToken?: string;
  user?: string;
}
export const authService = {
  login: (data: LoginData): Promise<AuthData> => {
    return client.post("accounts/login", data);
  },
  logout: (refreshToken: string) => {
    return client.post(
      "accounts/logout",
      { refreshToken },
      {
        headers: {
          Authorization: `Bearer ${accessTokenService.get()}`,
        },
      },
    );
  },
  refresh: (refreshToken: string): Promise<AuthData> =>
    client.post("accounts/refresh", { refreshToken }),
};
