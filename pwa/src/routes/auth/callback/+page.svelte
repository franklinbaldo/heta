<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores'; // To access URL query parameters
  import { goto } from '$app/navigation'; // For redirection
  import { base } from '$app/paths';
  import { authStore } from '$lib/authStore.js';

  let message = 'Processando autenticação...';
  let error = null;

  onMount(async () => {
    const queryParams = $page.url.searchParams;
    const code = queryParams.get('code');
    const ghError = queryParams.get('error'); // GitHub might return an error parameter
    const ghErrorDescription = queryParams.get('error_description');

    if (ghError) {
      error = ghErrorDescription || ghError;
      message = 'Falha na autenticação com o GitHub.';
      authStore.setError(error);
      // Optionally redirect after a delay or keep user on this page to see error
      setTimeout(() => {
        goto(`${base}/`);
      }, 5000);
      return;
    }

    if (code) {
      authStore.setAuthCode(code);
      message = 'Autenticação bem-sucedida! Redirecionando...';

      // **CONCEPTUAL NEXT STEP: Exchange code for an access token**
      // This is where you would typically send the `code` to your backend/serverless function
      // to exchange it for an access token. The backend would then securely store the token
      // or return necessary user info/session token to the PWA.
      // e.g., const response = await fetch(`${base}/api/auth/github`, { method: 'POST', body: JSON.stringify({ code }) });
      // const data = await response.json();
      // if (data.success) {
      //   authStore.setLoginSuccess(data.userName, data.token); // Or whatever your backend returns
      // } else {
      //   authStore.setError(data.message);
      // }

      // For now, we'll simulate a successful login by setting a mock user name
      // In a real app, this would come from the token exchange response.
      // We will also fetch the user's profile information from GitHub using the code (via a backend proxy in a real app).
      // For this example, we'll just use a placeholder name.
      // A real implementation would fetch user data from GitHub API using the obtained token.
      // For now, we simulate this by simply setting a generic username.
      // A more advanced version would use the code to get a token, then use the token to get user info.
      // This part requires a backend proxy for security.
      // For now, we'll just acknowledge the code and set a placeholder user.
      // In a real app, you'd call your backend here to exchange code for a token & get user details.
      // For demonstration, we'll assume the backend would return a username.
      // This is a MOCK. The real username would come from a backend call.
      const mockUserName = "Usuário GitHub"; // Placeholder
      authStore.setLoginSuccess(mockUserName, code);


      // Redirect to the main page
      setTimeout(() => {
        goto(`${base}/`);
      }, 1500); // Short delay to show success message

    } else {
      error = 'Nenhum código de autorização recebido do GitHub.';
      message = 'Falha na autenticação.';
      authStore.setError(error);
      setTimeout(() => {
        goto(`${base}/`);
      }, 5000);
    }
  });
</script>

<svelte:head>
  <title>Heta - Callback de Autenticação</title>
</svelte:head>

<div class="callback-container">
  <h2>{message}</h2>
  {#if error}
    <p class="error-message">Detalhes: {error}</p>
  {/if}
  <p><a href="{base}/">Voltar para a página inicial</a></p>
</div>

<style>
  .callback-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    text-align: center;
    padding: 2rem;
  }
  .error-message {
    color: red;
    margin-top: 1rem;
  }
  h2 {
    margin-bottom: 1rem;
  }
</style>
