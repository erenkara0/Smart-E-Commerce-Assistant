const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

const configuredApiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL?.trim();

export const API_BASE_URL = (
  configuredApiBaseUrl || DEFAULT_API_BASE_URL
).replace(/\/+$/, "");