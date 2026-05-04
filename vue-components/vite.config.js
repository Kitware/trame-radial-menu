export default {
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "radial_menu",
      formats: ["umd"],
      fileName: "radial_menu",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../src/radial_menu/module/serve",
    assetsDir: ".",
  },
};
