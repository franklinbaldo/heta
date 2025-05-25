# Heta PWA

This directory contains the SvelteKit-based Progressive Web App for the Heta project.

## Development

1.  `cd pwa`
2.  `npm install` (or your preferred package manager)
3.  `npm run dev`
4.  For local development involving GitHub OAuth:
    *   You must register a GitHub OAuth application.
    *   Set the `GITHUB_CLIENT_ID` placeholder in `pwa/src/lib/authStore.js` and potentially other places with your actual Client ID.
    *   Ensure your OAuth app's callback URL matches `http://localhost:<port>/auth/callback` (e.g., `http://localhost:5173/auth/callback`).

## GitHub OAuth Security - IMPORTANT

The current GitHub OAuth implementation in this PWA is **for client-side demonstration purposes only** and handles only the initial part of the OAuth flow (redirect to GitHub and receiving a temporary authorization `code`).

**Key Security Points:**

*   **Backend Required for Full OAuth Flow:** To securely exchange the temporary `code` for an access token and to make authenticated API calls to GitHub (e.g., to create issues, fetch user details beyond basic redirect info), a **backend component (like a serverless function) is essential.**
*   **Client Secret Protection:** The GitHub OAuth **Client Secret must NEVER be embedded in the PWA's frontend code.** It must reside only on the secure backend.
*   **Access Token Handling:** Access tokens, especially those with write permissions, should be managed by this backend proxy. Storing such tokens directly in the browser (e.g., `localStorage`) is a significant security risk.
*   **Current Limitations:** This PWA currently **does not** perform the secure token exchange or make authenticated API calls for actions like creating issues. The "logged in" state is based on successfully receiving the temporary code and uses mock user data.

Refer to the main project `README.md` and comments in `pwa/src/lib/authStore.js` for more details on the recommended secure architecture using a backend proxy for GitHub API interactions. This aligns with the original project vision of potentially using Netlify Edge Functions or similar for such tasks.
