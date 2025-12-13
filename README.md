# Budget Tracker CLI

A Python CLI tool for connecting to your RBC bank account via Plaid and pulling monthly statements.

## Setup

1. **Install dependencies with Poetry:**
   ```bash
   poetry install
   ```

2. **Configure Plaid API:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your Plaid credentials from [Plaid Dashboard](https://dashboard.plaid.com/):
   ```env
   PLAID_CLIENT_ID=your_client_id_here
   PLAID_SECRET=your_secret_here
   PLAID_PUBLIC_TOKEN_URL=https://secure.plaid.com/hl/
   ACCOUNT_TO_FILTER=RBC ION+ Visa
   ```

## Usage Flow

### Step 1: Link Your RBC Account

```bash
poetry run budget-tracker link
```

This generates a Plaid Link URL and opens it in your browser:
```
🔗 Link Token Created Successfully!
Link Token: link-sandbox-abc123...

📋 Next Steps:
1. Go to: https://secure.plaid.com/hl/abc123...
2. Select 'Royal Bank of Canada' from the institution list
3. For SANDBOX testing, use these credentials:
   Username: user_good
   Password: pass_good
4. Complete the linking process
5. Copy the public_token from the browser network tab
6. Use it with: budget-tracker exchange <public_token>

🌐 Opening Plaid Link in your browser...
```

### Step 2: Complete Account Linking in Browser

1. **Browser will open automatically** to the Plaid Link page
2. **Select "Royal Bank of Canada"** from the institution list
3. **Enter sandbox credentials:**
   - Username: `user_good`
   - Password: `pass_good`
4. **Select your accounts** and complete the linking process

### Step 3: Extract Public Token from Network Tab

**This is the critical step!** After successful linking:

1. **Keep browser DevTools open** (F12 or right-click → Inspect)
2. **Go to Network tab** in DevTools
3. **Complete the Plaid linking flow** 
4. **Look through the network requests** (usually one of the last 2-3 requests)
5. **Find a request with response containing `public_token`**
6. **Copy the public token** (starts with `public-sandbox-` or `public-development-`)

**Pro tip:** The public token is usually in a POST request response after you click "Continue" or "Done" in the Plaid interface.

### Step 4: Exchange Public Token for Access Token

```bash
poetry run budget-tracker exchange public-sandbox-abc123def456ghi789...
```

Expected output:
```
Exchanging public token...
✅ Success! Your RBC account is now linked and ready to use.
Item ID: item-abc123...

🎉 You can now pull your statements with: budget-tracker pull
```

### Step 5: Pull Bank Statements

```bash
# Pull current month statements
poetry run budget-tracker pull

# Pull specific month (YYYY-MM format)
poetry run budget-tracker pull --month 2025-01
```

Expected output:
```
📊 Fetching transactions from 2024-01-01 to 2024-01-31...
✅ Found 15 transactions for 2024-01

{
  "month": "2024-01",
  "accounts": [
    {
      "name": "Savings",
      "type": "depository",
      "balance": 1500.25
    }
  ],
  "transactions": [
    {
      "date": "2024-01-15",
      "description": "Tim Hortons",
      "amount": -4.50,
      "category": "FOOD_AND_DRINK"
    }
  ],
  "summary": {
    "totalIncome": 2500.00,
    "totalExpenses": 856.75,
    "netAmount": 1643.25,
    "transactionCount": 15
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `poetry run budget-tracker link` | Generate Plaid Link URL for account connection |
| `poetry run budget-tracker exchange <token>` | Exchange public token for access token |
| `poetry run budget-tracker pull` | Pull current month's transactions |
| `poetry run budget-tracker pull --month YYYY-MM` | Pull specific month's transactions |
| `poetry shell` | Activate virtual environment (then run commands without `poetry run`) |

## Troubleshooting

### "No linked account found"
- Make sure you completed the `exchange` step after linking
- Your access token is stored in `~/.budget-tracker/access-token.json`

### "Error creating link token"
- Check your `.env` file has correct Plaid credentials
- Ensure `PLAID_ENV=sandbox` for testing

### "Failed to pull statements"
- Your access token may have expired
- Re-run the linking and exchange process
- Check that your Plaid account is active

### Browser Link Not Working
- Ensure you're using the exact URL provided by the link command
- Try opening in an incognito/private browser window

## File Structure

```
src/budget_tracker/
├── cli.py               # Main CLI entry point (Typer app)
├── commands/            # Command implementations
│   ├── link.py          # Account linking command
│   ├── exchange.py      # Token exchange command
│   └── pull.py          # Statement pulling command
├── services/            # API clients
│   └── plaid_client.py  # Plaid API integration
└── utils/               # Utilities
    └── storage.py       # Token storage utilities
```

## Frontend Development

The Budget Tracker includes a React-based web interface served through FastAPI.

### Initial Setup

```bash
# Install frontend dependencies
cd src/budget_tracker_api/frontend
npm install
```

### Development Workflow

**Option 1: Auto-Rebuild Mode (Recommended - Single Command)**
```bash
./dev.sh
# Automatically rebuilds frontend on file changes and serves via FastAPI
# Visit http://localhost:8000
```

This script:
- Does an initial frontend build
- Starts frontend build in watch mode (auto-rebuilds on changes)
- Starts FastAPI server
- Press Ctrl+C to stop both

**Option 2: Manual Build Mode**
```bash
# Build the frontend once
cd src/budget_tracker_api/frontend
npm run build

# Start the API server (serves built React app)
cd ../../..
poetry run api-start

# Visit http://localhost:8000
# (Rebuild manually after frontend changes)
```

**Option 3: Vite Dev Server (Fastest Hot Reload)**

Open two terminal windows:

Terminal 1 - FastAPI Backend:
```bash
poetry run api-start
# Runs on http://localhost:8000
```

Terminal 2 - Vite Dev Server:
```bash
cd src/budget_tracker_api/frontend
npm run dev
# Runs on http://localhost:5173 with instant hot module reloading
# API requests are proxied to port 8000
```

With this setup, visit `http://localhost:5173` for the fastest feedback loop.

### Frontend Scripts

From `src/budget_tracker_api/frontend/`:

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run dev` | Start Vite dev server (port 5173) |
| `npm run build` | Build production bundle to `../app/public/` |
| `npm run build:watch` | Build in watch mode (auto-rebuilds on changes) |
| `npm run preview` | Preview production build locally |

## Development

### Linting and Formatting

```bash
# Run linting
poetry run ruff check .

# Auto-fix linting issues
poetry run ruff check --fix .

# Format code
poetry run ruff format .

# Type checking
poetry run mypy src/
```

## Security Notes

- Access tokens are stored locally in `~/.budget-tracker/`
- Never commit your `.env` file or share your Plaid credentials
- Use sandbox environment for testing
- Production tokens have stricter security requirements