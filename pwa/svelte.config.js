import adapter from '@sveltejs/adapter-static'; // For GitHub Pages deployment
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: null, // or 'index.html' or '200.html' if needed
      precompress: false,
      strict: true
    }),
    paths: {
      base: process.env.NODE_ENV === 'production' ? '/Heta' : '', // Adjust '/Heta' to your repo name if needed
    }
  }
};
export default config;
