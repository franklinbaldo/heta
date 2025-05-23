import adapter from '@sveltejs/adapter-static'; // Use adapter-static for GitHub Pages
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: null, // or 'index.html' or '200.html' if using SPA mode
      precompress: false,
      strict: true
    }),
    paths: {
      base: process.env.NODE_ENV === 'production' ? '/Heta' : '', // Adjust if your repo name is different
    }
  }
};
export default config;
