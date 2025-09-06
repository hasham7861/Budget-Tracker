import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { TransactionData } from 'plaid';

const CONFIG_DIR = path.join(os.homedir(), '.budget-tracker');
const ACCESS_TOKEN_FILE = path.join(CONFIG_DIR, 'access-token.json');

interface StoredTokenData {
  accessToken: string;
  itemId: string;
  createdAt: string;
}

export function saveAccessToken(accessToken: string, itemId: string) {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }

  const data: StoredTokenData = {
    accessToken,
    itemId,
    createdAt: new Date().toISOString(),
  };

  fs.writeFileSync(ACCESS_TOKEN_FILE, JSON.stringify(data, null, 2));
}

export function getAccessToken(): string | null {
  try {
    if (!fs.existsSync(ACCESS_TOKEN_FILE)) {
      return null;
    }

    const data: StoredTokenData = JSON.parse(fs.readFileSync(ACCESS_TOKEN_FILE, 'utf8'));
    return data.accessToken;
  } catch (error) {
    console.error('Error reading access token:', error);
    return null;
  }
}

export function hasAccessToken(): boolean {
  return getAccessToken() !== null;
}

export function getCachedTransactions(month: string): TransactionData | null {
  throw new Error('Not implemented');
}

export function setCachedTransactions(month: string, data: TransactionData): void {
  throw new Error('Not implemented');
}

export function cleanupOldCache(): void {
  throw new Error('Not implemented');
}