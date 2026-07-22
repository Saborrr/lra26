<div align="center">

<img src="frontend/public/icons/icon.svg" width="112" alt="LRA-26" />

# LRA-26 · Live Space Ranking

A secure space-themed competition platform for Web, iOS, Android, Telegram, and VK.

[Русский](README.md) · **English**

</div>

![LRA-26 application preview](docs/assets/app-preview.svg)

> Downloaded the repository as a ZIP? Double-click the root `index.html` file to open an interactive, self-contained UI preview with demo data. It requires no Python, Node.js, or database.

## Highlights

- Live public leaderboard powered by WebSockets with an HTTP fallback.
- Installable PWA for iPhone, iPad, and Android.
- Telegram Mini App, Telegram bot, and VK Mini App adapters.
- Participant dashboard with team progress and active quests.
- Administrator mission control for teams, quests, scores, and penalties.
- Super administrator console for accounts, roles, link codes, and the audit trail.
- PostgreSQL, Redis, Django Channels, React 19, and Docker Compose.

The production application is designed to be served at `https://gofaraway.mooo.com/lra26/`. Only the frontend proxy binds to localhost; the database, Redis, and Django remain inside a private Docker network.

See [the Russian README](README.md) and [deployment guide](docs/DEPLOYMENT.md) for complete setup instructions.

## Security

The project validates Telegram and VK signed launch data on the server, uses Argon2 passwords, short-lived access tokens, rotating HttpOnly refresh cookies, role-based permissions, throttling, database constraints, WebSocket origin validation, hardened containers, and an append-only application audit trail.

Please report vulnerabilities privately according to [SECURITY.md](SECURITY.md).

## Licensing

The source is available under the [PolyForm Noncommercial License 1.0.0](LICENSE). Personal, educational, and other noncommercial use is permitted while preserving the required author notice and original-project link. Commercial use, SaaS, resale, or revenue-supporting use requires a separate [commercial agreement](COMMERCIAL_LICENSE.md) with Aleksandr Fadeev. That agreement may use a fixed fee, subscription, or revenue-share royalty.

This is a **source-available** project, not OSI-approved open source.

## Author

**Aleksandr Fadeev** · [@Saborrr](https://github.com/Saborrr)

Noncommercial license: [PolyForm Noncommercial 1.0.0](LICENSE) · [Commercial terms](COMMERCIAL_LICENSE.md).
