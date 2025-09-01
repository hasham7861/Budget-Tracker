# Budget Tracker CLI - Claude Code Context

## Project Overview
A TypeScript-based CLI tool for connecting to RBC bank accounts via Plaid API and pulling monthly transaction statements.

## Tech Stack
- **Language**: TypeScript (ES2020 target)
- **Runtime**: Node.js
- **CLI Framework**: Commander.js
- **Banking API**: Plaid (Canadian market focus)
- **Build Tool**: TypeScript compiler (tsc)
- **Development**: ts-node, nodemon

## Dependencies
### Production
- `commander@^14.0.0` - CLI command framework
- `dotenv@^17.2.1` - Environment variable management
- `plaid@^38.0.0` - Plaid API client

### Development
- `typescript@^5.9.2` - TypeScript compiler
- `ts-node@^10.9.2` - TypeScript execution
- `nodemon@^3.1.10` - Development file watching
- `@types/node@^24.3.0` - Node.js type definitions

## Project Structure
```
src/
├── commands/
│   ├── link.ts          # Account linking via Plaid Link
│   └── pull.ts          # Transaction statement retrieval
├── services/
│   └── plaid.ts         # Plaid API integration & token exchange
├── utils/
│   └── storage.ts       # Local token storage (~/.budget-tracker/)
└── index.ts             # CLI entry point with Commander setup
```

## Commands & Scripts
```bash
# Development
npm run dev              # Run with ts-node
npm run watch           # Development with auto-reload

# Build & Production
npm run build           # Compile TypeScript
npm run start           # Run compiled version

# CLI Commands
npm run dev link                    # Generate Plaid Link URL
npm run dev exchange <token>        # Exchange public token for access token
npm run dev pull                    # Pull current month statements
npm run dev pull -m YYYY-MM         # Pull specific month
npm run dev pull -f csv             # Output in CSV format
```

## Environment Configuration
Requires `.env` file with Plaid credentials:
```env
PLAID_ENV=sandbox                   # Environment (sandbox/development/production)
PLAID_CLIENT_ID=your_client_id      # From Plaid Dashboard
PLAID_SECRET=your_secret           # From Plaid Dashboard
PLAID_PRODUCTS=transactions         # Plaid product access
PLAID_COUNTRY_CODES=CA             # Canada focus
```

## Code Conventions
- **Strict TypeScript** with all strict compiler options enabled
- **CommonJS modules** for Node.js compatibility
- **Async/await** for asynchronous operations
- **Error handling** with try/catch blocks and user-friendly messages
- **CLI UX** with emojis and clear status messages (✅, ❌, 🔗, 📊, 🎉)
- **Token storage** in user home directory (`~/.budget-tracker/`)

## Development Workflow
1. **Environment Setup**: Configure `.env` with Plaid sandbox credentials
2. **Account Linking**: Use `link` command → complete browser flow → extract public token
3. **Token Exchange**: Use `exchange` command to get persistent access token
4. **Data Retrieval**: Use `pull` command to fetch transaction data
5. **Testing**: Currently uses Plaid sandbox with test credentials (`user_good`/`pass_good`)

## Current Roadmap Status
- ✅ **Phase 1**: Basic CLI structure with Commander.js
- ✅ **Phase 2**: Plaid integration for RBC account linking
- ✅ **Phase 3**: Transaction pulling with date/format options
- 🔄 **Phase 4**: Enhanced data processing and categorization
- 📋 **Future**: Multi-bank support, data visualization, budgeting features

## Security Notes
- Access tokens stored locally, never committed to repository
- Sandbox environment for development/testing
- Canadian banking focus (RBC initially)
- No credentials logged or exposed in error messages

## Testing Strategy
- Currently manual testing with Plaid sandbox
- No automated test suite yet (npm test returns error)
- Browser-based testing for Plaid Link flow

## Build Configuration
- TypeScript compilation to `dist/` directory
- Source maps and declaration files generated
- Binary entry point: `dist/index.js`
- Strict type checking with consistent casing enforcement