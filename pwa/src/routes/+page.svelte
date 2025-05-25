<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';
  import OfferList from '$lib/OfferList.svelte';
  import { authStore, initializeAuth } from '$lib/authStore.js'; // Import the store

  // Offer listing state
  let offers = [];
  let isLoadingOffers = true;
  let offersError = null;

  // Subscribe to auth store for reactive UI updates
  // $: syntax creates a reactive statement
  let currentAuth;
  authStore.subscribe(value => {
    currentAuth = value;
  });

  function handleLogin() {
    authStore.login(base); // Pass the base path
  }

  function handleLogout() {
    authStore.logout();
  }

  onMount(async () => {
    // initializeAuth(); // Initialize auth state from localStorage - MOVED TO +layout.svelte

    // Fetch offers
    try {
      const response = await fetch(`${base}/_data/ofertas_ativas.json`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      offers = await response.json();
    } catch (e) {
      console.error("Failed to fetch offers:", e);
      offersError = e.message;
    } finally {
      isLoadingOffers = false;
    }
  });
</script>

<svelte:head>
  <title>Heta - Ofertas Ativas</title>
</svelte:head>

<header>
  <div class="logo-title">
    <h1>Heta - Ofertas de Alimentos</h1>
  </div>
  <div class="auth-section">
    {#if currentAuth && currentAuth.isLoggedIn}
      <p>Bem-vindo(a), {currentAuth.userName}! <button on:click={handleLogout}>Logout</button></p>
    {:else}
      <button on:click={handleLogin}>Login com GitHub</button>
    {/if}
    {#if currentAuth && currentAuth.error}
      <p class="error-message">Erro de autenticação: {currentAuth.error}</p>
    {/if}
  </div>
</header>

<main>
  {#if isLoadingOffers}
    <p>Carregando ofertas...</p>
  {:else if offersError}
    <p class="error-message">Erro ao carregar ofertas: {offersError}</p>
    <p>Por favor, verifique se o arquivo <code>_data/ofertas_ativas.json</code> existe e está acessível.</p>
  {:else}
    <OfferList {offers} />
  {/if}
</main>

<style>
  /* Styles remain the same as previous step */
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #f0f0f0;
    border-bottom: 1px solid #ddd;
  }

  .logo-title h1 {
    margin: 0;
    font-size: 1.5rem;
    color: #333;
  }

  .auth-section {
    display: flex;
    align-items: center;
  }

  .auth-section p {
    margin-right: 1rem;
  }

  .auth-section button {
    padding: 0.5rem 1rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .auth-section button:hover {
    background-color: #0056b3;
  }

  main {
    padding: 1rem;
  }

  .error-message {
    color: red;
    text-align: center;
  }

  h1 { 
    color: #333;
    text-align: center;
    margin-bottom: 1rem; 
  }

  p { 
    text-align: center;
  }
</style>
