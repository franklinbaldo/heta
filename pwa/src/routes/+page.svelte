<script>
  import { onMount } from 'svelte';
  let ofertas = [];
  let error = null;
  let base_path = '';

  // Determine base path for fetching data, matching SvelteKit's base path logic
  // This is a simplified approach. For a robust solution, consider passing base path from build or environment.
  if (typeof window !== 'undefined' && window.location.pathname.includes('/Heta')) {
     base_path = '/Heta';
  }

  onMount(async () => {
    try {
      // Adjust the path to where ofertas_ativas.json will be relative to the deployed PWA's root
      // Assuming ofertas_ativas.json is copied to the root of the build output (e.g., 'build/_data/ofertas_ativas.json')
      // or served from a location accessible relative to the deployed PWA.
      // For GitHub Pages, if _data is at the root of the gh-pages branch, this might be base_path + '/_data/ofertas_ativas.json'
      // This needs to be aligned with how data is made available to the PWA.
      // For now, let's assume it will be in a '_data' folder at the root of the deployment.
      const response = await fetch(`${base_path}/_data/ofertas_ativas.json`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      ofertas = await response.json();
    } catch (e) {
      error = e.message;
      console.error("Failed to load ofertas:", e);
      // Fallback: try to load from a fixed root path if the base_path attempt fails (e.g. local dev without repo name in path)
      try {
         const fallbackResponse = await fetch('/_data/ofertas_ativas.json');
         if (!fallbackResponse.ok) {
             throw new Error(`HTTP error (fallback)! status: ${fallbackResponse.status}`);
         }
         ofertas = await fallbackResponse.json();
         error = null; // Clear previous error if fallback succeeds
      } catch (e2) {
         error = e2.message;
         console.error("Failed to load ofertas (fallback):", e2);
      }
    }
  });
</script>

<h1>Ofertas de Excedentes</h1>

{#if error}
  <p style="color: red;">Erro ao carregar ofertas: {error}</p>
  <p>Tentando carregar de: <code>{base_path}/_data/ofertas_ativas.json</code> e <code>/_data/ofertas_ativas.json</code></p>
{/if}

{#if ofertas.length === 0 && !error}
  <p>Nenhuma oferta disponível no momento.</p>
{:else if ofertas.length > 0}
  <ul>
    {#each ofertas as oferta}
      <li>
        <strong>{oferta.item}</strong> ({oferta.quantidade}) - Validade: {oferta.validade}
        <br>
        <small>Escola (INEP): {oferta.escola_codinep} - Issue: #{oferta.issue_number}</small>
        <br>
        <small>Status: {oferta.status}</small>
        {#if oferta.observacoes}<br><small>Obs: {oferta.observacoes}</small>{/if}
      </li>
    {/each}
  </ul>
{/if}

<style>
  ul { list-style-type: none; padding: 0; }
  li { margin-bottom: 1em; padding: 0.5em; border: 1px solid #eee; }
</style>
