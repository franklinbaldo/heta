<script>
  import { browser } from '$app/environment';
  import { initializeAuth } from '$lib/authStore.js';

  if (browser) {
    initializeAuth();
  }
</script>

<slot></slot>
