const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

function setCookie(name: string, value: string, maxAgeSeconds: number) {
  if (typeof document === "undefined") return;
  document.cookie = `${name}=${encodeURIComponent(value)}; Path=/; Max-Age=${maxAgeSeconds}; SameSite=Lax`;
}

function deleteCookie(name: string) {
  if (typeof document === "undefined") return;
  document.cookie = `${name}=; Path=/; Max-Age=0; SameSite=Lax`;
}

function getCookie(name: string) {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

export function saveAuthTokens(payload: { access_token?: string | null; refresh_token?: string | null }) {
  if (typeof window === "undefined") return;

  if ("access_token" in payload) {
    if (payload.access_token) {
      localStorage.setItem(ACCESS_TOKEN_KEY, payload.access_token);
      setCookie(ACCESS_TOKEN_KEY, payload.access_token, 60 * 60 * 24 * 7);
    } else {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      deleteCookie(ACCESS_TOKEN_KEY);
    }
  }

  if ("refresh_token" in payload) {
    if (payload.refresh_token) {
      localStorage.setItem(REFRESH_TOKEN_KEY, payload.refresh_token);
      setCookie(REFRESH_TOKEN_KEY, payload.refresh_token, 60 * 60 * 24 * 30);
    } else {
      localStorage.removeItem(REFRESH_TOKEN_KEY);
      deleteCookie(REFRESH_TOKEN_KEY);
    }
  }
}

export function clearAuthTokens() {
  if (typeof window === "undefined") return;

  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  deleteCookie(ACCESS_TOKEN_KEY);
  deleteCookie(REFRESH_TOKEN_KEY);
}

export function getStoredAccessToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ACCESS_TOKEN_KEY) ?? getCookie(ACCESS_TOKEN_KEY);
}

export function getStoredRefreshToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(REFRESH_TOKEN_KEY) ?? getCookie(REFRESH_TOKEN_KEY);
}
