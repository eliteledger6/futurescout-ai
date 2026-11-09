/** @type {import('next').NextConfig} */
// The dashboard calls the API as `/api/...` on its own origin (NEXT_PUBLIC_API_URL empty, the default) and Next
// proxies those calls to the FastAPI server at API_INTERNAL_URL. One address is enough to share the site (a tunnel,
// a VPS, a container), and no CORS is involved. Set NEXT_PUBLIC_API_URL to call an API directly instead.
const apiInternal = process.env.API_INTERNAL_URL || "http://127.0.0.1:8000";

const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  devIndicators: false, // hide the dev-mode "N" badge (also keeps demo recordings clean)
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${apiInternal}/api/:path*` }];
  },
};

export default nextConfig;
