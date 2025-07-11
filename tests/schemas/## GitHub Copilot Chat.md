## GitHub Copilot Chat

- Extension Version: 0.28.5 (prod)
- VS Code: vscode/1.101.2
- OS: Windows

## Network

User Settings:
```json
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": true,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 20.201.28.148 (16 ms)
- DNS ipv6 Lookup: Error (8 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (14 ms)
- Electron fetch (configured): HTTP 200 (3870 ms)
- Node.js https: HTTP 200 (4703 ms)
- Node.js fetch: timed out after 10 seconds
- Helix fetch: HTTP 200 (2333 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.114.22 (5 ms)
- DNS ipv6 Lookup: Error (2 ms): getaddrinfo ENOTFOUND api.individual.githubcopilot.com
- Proxy URL: None (12 ms)
- Electron fetch (configured): HTTP 200 (217 ms)
- Node.js https: timed out after 10 seconds
- Node.js fetch: timed out after 10 seconds
- Helix fetch: HTTP 200 (9409 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).
