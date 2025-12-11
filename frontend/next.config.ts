import type { NextConfig } from "next";
import path from "path";
import dotenv from "dotenv";

// Load environment variables from root .env file
dotenv.config({ path: path.resolve(__dirname, "../.env") });

const nextConfig: NextConfig = {
  cacheComponents: true,
};

export default nextConfig;
