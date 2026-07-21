import axios, { AxiosError } from "axios";
import humps from "humps";

import { accessTokenService } from "@/services/accessTokenService";
import { authService } from "@/services/authService";
import { refreshTokenService } from "@/services/refreshTokenService";

export const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});


httpClient.interceptors.request.use((config) => {
  const accessToken = accessTokenService.get();

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  if (config.data) {
    config.data = humps.decamelizeKeys(config.data);
  }

  if (config.params) {
    config.params = humps.decamelizeKeys(config.params);
  }

  return config;
});


httpClient.interceptors.response.use(
  (response) => {
    response.data = humps.camelizeKeys(response.data);

    return response;
  },

  async (error: AxiosError) => {
    if (error.response?.status !== 401) {
      throw error;
    }

    const originalRequest = error.config!;

   const refreshToken = refreshTokenService.get();

if (!refreshToken) {
  throw error;
}

const { accessToken } = await authService.refresh(refreshToken);

accessTokenService.save(accessToken);

return httpClient.request(originalRequest);
  }
);