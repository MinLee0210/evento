import { fileURLToPath, URL } from "url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";
import dotenv from 'dotenv';

dotenv.config(); // load env vars from .env
// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: "::",
    port: "3000",
  },
  define: {
    BACKEND_URL: `"${process.env.BACKEND_URL}"`,
    BACKEND_URL_SEARCH: `"${process.env.BACKEND_URL_SEARCH}"`,
    BACKEND_URL_GET_IMAGE: `"${process.env.BACKEND_URL_GET_IMAGE}"`,
  },
  plugins: [react()],
  resolve: {
    alias: [
      {
        find: "@",
        replacement: fileURLToPath(new URL("./src", import.meta.url)),
      },
      {
        find: "lib",
        replacement: resolve(__dirname, "lib"),
      },
    ],
  },
});
