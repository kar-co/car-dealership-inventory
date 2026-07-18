const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "/api";

export async function request(path, { token, ...options } = {}) {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || "Something went wrong. Please try again.");
  }

  return response.status === 204 ? null : response.json();
}
