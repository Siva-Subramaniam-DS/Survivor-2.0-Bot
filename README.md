# Survivor 2.0 Bot

A Discord bot that helps run tournaments on the Survivor Modern Warships server. It balances teams, assigns players to rooms, handles weekend check-ins, announces winners and logs to Google Sheets.

## Slash commands

| Command | What it does |
|---|---|
| `/team_balance` | Balance two teams based on player levels |
| `/warzone-cc-all` | Assign players to warzone rooms for a round (5v5 down to 1v1) |
| `/warzone-winners` | Announce warzone tournament winners |
| `/saturday-check-in` | Saturday check-in for players |
| `/sunday-check-in` | Sunday check-in for players |
| `/remove-joined-roles` | Remove Joined roles after the check-in period ends |
| `/support-ars` | Add, remove or swap support roles |
| `/bot-status` | Check bot permissions and status (admin only) |
| `/sync-commands` | Manually sync slash commands (admin only) |

## Requirements

- Python 3.11
- A Discord bot token
- A Google service account with access to the tournament spreadsheet

## Setup

```bash
pip install -r requirements.txt
```

1. Copy `env.example` to `.env` and set `DISCORD_TOKEN`.
2. Provide Google credentials in one of two ways:
   - copy `credentials.json.example` to `credentials.json` and fill it in, or
   - set the `GOOGLE_CREDENTIALS` environment variable to the service account JSON.
3. Start the bot:

```bash
python app.py
```

Never commit `.env` or `credentials.json`.

## Deployment

- **Railway:** see [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md). `railway.json`, `nixpacks.toml` and `Procfile` are included.
- **Docker:** a `Dockerfile` is included, with `docker-run.sh` and `docker-run.bat` helpers.

## Troubleshooting

- Slash commands not showing up: see [RAILWAY_COMMAND_SYNC_FIX.md](RAILWAY_COMMAND_SYNC_FIX.md) or run `/sync-commands`.
- Google Sheets errors: see [CHECK_CREDENTIALS.md](CHECK_CREDENTIALS.md).

## Tech stack

discord.py, gspread, google-auth, python-dotenv.
