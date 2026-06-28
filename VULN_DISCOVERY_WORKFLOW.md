# Bug Bounty Discovery Methodology

## 1. Environment Sandbox
All reconnaissance is performed within the isolated Fargate environment. No traffic originates from the local host, ensuring research anonymity and environment safety.

## 2. Target Ingestion
Targets are managed via the MCP `get_watchlists` tool. The agent automatically iterates through these to initiate `nuclei` scans and `ffuf` directory brute-forcing.

## 3. Reporting Pipeline
Discovered vulnerabilities are piped through the Python shield, sanitized for JSON format, and pushed to the `sovereign-vault` GitHub repository using a predefined YAML template.
