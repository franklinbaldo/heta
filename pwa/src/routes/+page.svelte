<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths'; // For correct base path handling
  import OfferList from '$lib/OfferList.svelte'; // Adjusted path to $lib

  let offers = [];
  let isLoading = true;
  let error = null;

  onMount(async () => {
    try {
      // Construct the path carefully. If _data is at the root of the gh-pages deployment,
      // and base is '/Heta', the path will be '/Heta/_data/ofertas_ativas.json'.
      // If base is empty (dev), it will be '/_data/ofertas_ativas.json'.
      // The key is that `_data` must be copied to the output directory at the correct relative location.
      // For SvelteKit static adapter, files from the `static` directory in pwa are copied to the root of the build.
      // So, we should place _data there or ensure it's copied by the build process.
      // For now, let's assume _data will be at the root relative to the domain.
      // A better approach for SvelteKit is to use endpoints or load functions,
      // but for simple static JSON fetch:
      const response = await fetch(`${base}/_data/ofertas_ativas.json`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      offers = await response.json();
    } catch (e) {
      console.error("Failed to fetch offers:", e);
      error = e.message;
    } finally {
      isLoading = false;
    }
  });
</script>

<svelte:head>
  <title>Heta - Ofertas Ativas</title>
</svelte:head>

<h1>Ofertas de Alimentos Disponíveis</h1>

{#if isLoading}
  <p>Carregando ofertas...</p>
{:else if error}
  <p style="color: red;">Erro ao carregar ofertas: {error}</p>
  <p>Por favor, verifique se o arquivo <code>_data/ofertas_ativas.json</code> existe e está acessível no caminho esperado.</p>
{:else}
  <OfferList {offers} />
{/if}

<style>
  h1 {
    color: #333;
    text-align: center;
    margin-bottom: 2rem;
  }
  p {
    text-align: center;
  }
</style>
