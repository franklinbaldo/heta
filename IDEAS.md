# Heta Project - Ideas for Enhancement & Value Addition

This document lists actionable and high-impact ideas for improving the Heta project.

## PWA (Progressive Web App) Enhancements

1.  **Implement Basic Offer Listing:**
    *   **Description:** Develop the initial PWA interface to fetch and display active food offers from `_data/ofertas_ativas.json`. This is a foundational step mentioned in the 7-day roadmap (Day 5).
    *   **Impact:** Provides a user-friendly way for entities to view available donations.
    *   **Actionable Steps:**
        *   Choose a frontend framework (SvelteKit or Vue, as mentioned in `deploy_pwa.yml`).
        *   Set up the basic PWA structure.
        *   Implement JavaScript to fetch `_data/ofertas_ativas.json`.
        *   Create UI components to display each offer's details (item, quantity, validity, school).

2.  **GitHub OAuth Integration for PWA:**
    *   **Description:** Allow users to authenticate via GitHub within the PWA. This would enable them to create new offers (submit issues) or comment on existing offers (to reserve/collect) directly from the PWA interface, rather than going to GitHub. (Corresponds to "Próximos saltos pós-MVP" #1).
    *   **Impact:** Streamlines user workflow and improves user experience significantly.
    *   **Actionable Steps:**
        *   Research GitHub OAuth implementation for the chosen PWA framework.
        *   Implement the OAuth flow.
        *   Develop PWA forms/buttons to trigger issue creation and commenting via the GitHub API using the authenticated user's token.

3.  **PWA: Real-time Updates / Notifications (Optional - Advanced):**
    *   **Description:** Explore mechanisms for providing real-time updates in the PWA when new offers are added or existing ones are updated. This could involve polling or, if a light backend is considered, WebSockets.
    *   **Impact:** Ensures users have the most current information without manual refreshes.
    *   **Actionable Steps:**
        *   Evaluate feasibility given the "backendless" approach (e.g., GitHub Actions writing to a file that the PWA frequently polls, or using a serverless function for notifications).

## Backend Script & Workflow Enhancements

4.  **Geo-matching for Donations:**
    *   **Description:** Enhance `update_oferta_status.py` (or create a new script) to automatically recommend the nearest registered entity when a new offer is made. This would involve storing entity location data (e.g., address or coordinates, obtained during registration) and calculating distances. (Corresponds to "Próximos saltos pós-MVP" #2).
    *   **Impact:** Optimizes logistics and reduces food waste by facilitating quicker pickups.
    *   **Actionable Steps:**
        *   Update `cadastro_entidade.yml` to include address/postal code or latitude/longitude.
        *   Modify the entity registration process to store this location data (e.g., in a new JSON file `_data/entidades.json`).
        *   Implement a geo-coding function (if addresses are collected) or distance calculation logic in the Python script.
        *   When a new offer is processed, the script could identify nearby entities and potentially @-mention them in a comment on the offer issue.

5.  **Data Validation & Schema Enforcement:**
    *   **Description:** Implement robust data validation for all incoming data, especially from GitHub Issues and the SIGPC XML. Use `jsonschema` (mentioned in the 7-day roadmap, Day 4) to validate `_data/ofertas_ativas.json` and other JSON files.
    *   **Impact:** Improves data quality, reduces errors in processing, and makes the system more resilient.
    *   **Actionable Steps:**
        *   Define JSON schemas for `ofertas_ativas.json`, `potencial_vencimento.json`, and any new data files (e.g., `entidades.json`).
        *   Integrate schema validation into `create_oferta_from_issue.py`, `parse_sigpc.py`, and `update_oferta_status.py`.
        *   Consider adding validation to the GitHub Issue forms themselves if possible (e.g., regex for date formats).

6.  **Improved Error Handling & Logging in Scripts:**
    *   **Description:** Enhance all Python scripts with more comprehensive error handling (try-except blocks) and logging. Log important events and errors to GitHub Actions console output, or potentially to a dedicated log file (though this adds complexity).
    *   **Impact:** Makes debugging easier and provides better insight into workflow execution.
    *   **Actionable Steps:**
        *   Review all Python scripts for error handling.
        *   Implement `try-except` blocks around file operations, API calls, and data parsing.
        *   Use the `logging` module for structured logging.

## Data Management & Visualization

7.  **Dashboard for Donation History:**
    *   **Description:** Create interactive dashboards using Vega-Lite (or similar) to render data from `_data/historico_doacoes.csv` directly in the PWA. (Corresponds to "Próximos saltos pós-MVP" #3).
    *   **Impact:** Provides transparency and allows stakeholders to visualize the project's impact.
    *   **Actionable Steps:**
        *   Ensure `historico_doacoes.csv` captures relevant data points for visualization.
        *   Integrate a charting library like Vega-Lite into the PWA.
        *   Develop components to display charts (e.g., donations over time, by school, by entity type).

8.  **Data Export in Open Standards:**
    *   **Description:** Implement functionality to export the donation history (`_data/historico_doacoes.csv`) in formats like Open Refine/CKAN. (Corresponds to "Próximos saltos pós-MVP" #4).
    *   **Impact:** Promotes data sharing and interoperability with external transparency platforms.
    *   **Actionable Steps:**
        *   Research the specific requirements for Open Refine and CKAN data formats.
        *   Develop a Python script (or add to an existing one) that can be manually triggered or run on a schedule to convert `historico_doacoes.csv` to these formats.
        *   Make the exported files available for download, perhaps via the PWA or a link in the README.

## Security & Scalability

9.  **Refine Access Control for Issues:**
    *   **Description:** Review the current approach (restricting issues to collaborators or private repo) and explore if GitHub's newer "fine-grained personal access tokens" or specific issue form permissions could offer more nuanced control, especially if the PWA interacts with issues via API.
    *   **Impact:** Enhances security and manageability as the project grows.
    *   **Actionable Steps:**
        *   Research current best practices for GitHub API authentication and authorization for PWAs or automated scripts.
        *   Document recommendations for managing access.

10. **Input Sanitization for Scripts:**
    *   **Description:** Ensure all data read from external sources (GitHub Issues, comments, XML files) is properly sanitized before being processed or stored by the Python scripts to prevent potential injection attacks or data corruption.
    *   **Impact:** Critical for security and data integrity.
    *   **Actionable Steps:**
        *   Review all points where scripts ingest external data.
        *   Implement appropriate sanitization techniques (e.g., stripping unwanted characters, validating data types).

## Documentation

11. **Developer/Contributor Guide:**
    *   **Description:** Create a `CONTRIBUTING.md` file with guidelines for setting up the development environment, understanding the workflow, and contributing code or new ideas.
    *   **Impact:** Facilitates onboarding new contributors and ensures consistency.
    *   **Actionable Steps:**
        *   Document setup steps (Python version, dependencies).
        *   Explain the purpose of each script and workflow.
        *   Outline coding standards or contribution process.
