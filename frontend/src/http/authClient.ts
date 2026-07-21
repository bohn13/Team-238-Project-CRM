import axios from "axios";
import humps from "humps";

export const authClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

authClient.interceptors.request.use((config) => {
  if (config.data) {
    config.data = humps.decamelizeKeys(config.data);
  }

  if (config.params) {
    config.params = humps.decamelizeKeys(config.params);
  }

  return config;
});

authClient.interceptors.response.use((response) => {
  response.data = humps.camelizeKeys(response.data);

  return response;
});