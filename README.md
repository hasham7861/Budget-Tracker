# Budget Tracker CLI

A CLI tool for connecting to your RBC bank account via Plaid and pulling monthly statements.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure Plaid API:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your Plaid credentials from [Plaid Dashboard](https://dashboard.plaid.com/):
   ```env
   PLAID_ENV=sandbox
   PLAID_CLIENT_ID=your_client_id_here
   PLAID_SECRET=your_secret_here
   PLAID_PRODUCTS=transactions
   PLAID_COUNTRY_CODES=CA
   ```

3. **Build the project:**
   ```bash
   npm run build
   ```

## Usage Flow

### Step 1: Link Your RBC Account

```bash
npm run dev link
```

This generates a Plaid Link URL like:
```
🔗 Link Token Created Successfully!
Link Token: link-sandbox-abc123...

📋 Next Steps:
1. Go to: https://secure.plaid.com/hl/abc123...
```

### Step 2: Complete Account Linking

1. **Open the provided URL** in your browser
2. **Select "Royal Bank of Canada"** from the institution list
3. **Enter sandbox credentials:**
   - Username: `user_good`
   - Password: `pass_good`
4. **Complete the linking process** by selecting accounts

### Step 3: Extract Public Token

After successful linking, you'll see a success page. To get the public token:

1. **Open browser DevTools** (F12 or right-click → Inspect)
2. **Go to Network tab**
3. **Look for network requests** during the success page load
4. **Find the request** that returns a response containing `public_token`
5. **Copy the public token** (starts with `public-sandbox-` or `public-development-`)

Alternative method:
- Some success pages display the token directly in the URL or on the page
- Look for a string like: `public-sandbox-abc123def456ghi789...`

### Step 4: Exchange Public Token

```bash
npm run dev exchange public-sandbox-abc123def456ghi789...
```

Expected output:
```
Exchanging public token...
✅ Success! Your RBC account is now linked and ready to use.
Item ID: item-abc123...

🎉 You can now pull your statements with: npm run dev pull
```

### Step 5: Pull Bank Statements

```bash
# Pull current month statements
npm run dev pull

# Pull specific month
npm run dev pull -m 2024-01

# Get CSV format
npm run dev pull -f csv

# Specific month in CSV
npm run dev pull -m 2024-01 -f csv
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
| `npm run dev link` | Generate Plaid Link URL for account connection |
| `npm run dev exchange <token>` | Exchange public token for access token |
| `npm run dev pull` | Pull current month's transactions |
| `npm run dev pull -m YYYY-MM` | Pull specific month's transactions |
| `npm run dev pull -f csv` | Output in CSV format |

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
src/
├── commands/
│   ├── link.ts          # Account linking command
│   └── pull.ts          # Statement pulling command
├── services/
│   └── plaid.ts         # Plaid API integration
├── utils/
│   └── storage.ts       # Token storage utilities
└── index.ts             # CLI entry point
```

## Security Notes

- Access tokens are stored locally in `~/.budget-tracker/`
- Never commit your `.env` file or share your Plaid credentials
- Use sandbox environment for testing
- Production tokens have stricter security requirements