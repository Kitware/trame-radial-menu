import vue from "@vitejs/plugin-vue";

export default {
  plugins: [vue()],
  base: "./",
  resolve: {
    alias: {
      "@": "./src",
    },
  },
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_radial_menu",
      formats: ["umd"],
      fileName: "trame_radial_menu",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../src/trame_radial_menu/module/serve",
    assetsDir: ".",
  },
};
