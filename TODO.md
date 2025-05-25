# Heta Project - TODO List (Prioritized for Societal Value)

This list tracks key development tasks for the Heta project, focusing on ideas deemed most valuable to society.

## Core Functionality & Accessibility

- [x] **Implement Basic Offer Listing in PWA:**
    - Develop the initial PWA interface to fetch and display active food offers from `_data/ofertas_ativas.json`.
    - *Value: Provides a user-friendly way for entities to view available donations.*

- [ ] **GitHub OAuth Integration for PWA:**
    - Allow users to authenticate via GitHub within the PWA to create/comment on offers directly.
    - *Value: Streamlines user workflow, improves accessibility, and encourages participation.*

## Efficiency & Food Rescue Maximization

- [ ] **Geo-matching for Donations:**
    - Enhance backend scripts to automatically recommend the nearest registered entity when a new offer is made.
    - *Value: Optimizes logistics, reduces food waste by facilitating quicker pickups, and distributes food efficiently.*

## System Reliability & Trust

- [ ] **Data Validation & Schema Enforcement:**
    - Implement robust data validation for all incoming data (GitHub Issues, SIGPC XML) and for internal JSON files using schemas.
    *   *Value: Improves data quality, reduces errors, and makes the system more resilient and trustworthy.*

- [ ] **Input Sanitization for Scripts:**
    - Ensure all data read from external sources is properly sanitized before processing to prevent security vulnerabilities and data corruption.
    *   *Value: Critical for security, data integrity, and maintaining user trust.*

## Transparency & Community

- [ ] **Dashboard for Donation History:**
    - Create interactive dashboards in the PWA to render data from `_data/historico_doacoes.csv`.
    - *Value: Promotes transparency, allows visualization of project impact, and encourages support.*

- [ ] **Developer/Contributor Guide:**
    - Create a `CONTRIBUTING.md` with guidelines for setup, understanding workflows, and contributing.
    - *Value: Facilitates project evolution, maintenance, and broader community involvement.*
