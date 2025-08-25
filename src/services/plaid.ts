import { Configuration, PlaidApi, PlaidEnvironments } from 'plaid';
import * as dotenv from 'dotenv';

dotenv.config();

const configuration = new Configuration({
  basePath: PlaidEnvironments[process.env.PLAID_ENV as keyof typeof PlaidEnvironments],
  baseOptions: {
    headers: {
      'PLAID-CLIENT-ID': process.env.PLAID_CLIENT_ID,
      'PLAID-SECRET': process.env.PLAID_SECRET,
    },
  },
});

export const plaidClient = new PlaidApi(configuration);

export const plaidConfig = {
  clientId: process.env.PLAID_CLIENT_ID!,
  secret: process.env.PLAID_SECRET!,
  env: process.env.PLAID_ENV!,
  products: process.env.PLAID_PRODUCTS?.split(',') || ['transactions'],
  countryCodes: process.env.PLAID_COUNTRY_CODES?.split(',') || ['CA'],
};

export async function createLinkToken(userId: string = 'test-user') {
  try {
    const response = await plaidClient.linkTokenCreate({
      user: {
        client_user_id: userId,
      },
      client_name: 'Budget Tracker',
      products: plaidConfig.products as any,
      country_codes: plaidConfig.countryCodes as any,
      language: 'en',
      hosted_link: {},
    });
    
    return {
      linkToken: response.data.link_token,
      hostedLinkUrl: response.data.hosted_link_url,
    };
  } catch (error) {
    console.error('Error creating link token:', error);
    throw error;
  }
}

export async function exchangePublicToken(publicToken: string) {
  try {
    const response = await plaidClient.itemPublicTokenExchange({
      public_token: publicToken,
    });
    
    return {
      accessToken: response.data.access_token,
      itemId: response.data.item_id,
    };
  } catch (error) {
    console.error('Error exchanging public token:', error);
    throw error;
  }
}

export async function getAccounts(accessToken: string) {
  try {
    const response = await plaidClient.accountsGet({
      access_token: accessToken,
    });
    
    return response.data.accounts.map(account => ({
      accountId: account.account_id,
      name: account.name,
      officialName: account.official_name,
      type: account.type,
      subtype: account.subtype,
      balance: {
        available: account.balances.available,
        current: account.balances.current,
        currency: account.balances.iso_currency_code,
      },
    }));
  } catch (error) {
    console.error('Error fetching accounts:', error);
    throw error;
  }
}

export async function getTransactions(accessToken: string, startDate: string, endDate: string) {
  try {
    const response = await plaidClient.transactionsGet({
      access_token: accessToken,
      start_date: startDate,
      end_date: endDate,
    });
    
    return response.data.transactions.map(transaction => ({
      transactionId: transaction.transaction_id,
      accountId: transaction.account_id,
      amount: transaction.amount,
      date: transaction.date,
      name: transaction.merchant_name || transaction.original_description,
      category: transaction.personal_finance_category?.primary || 'Other',
      subcategory: transaction.personal_finance_category?.detailed || null,
    }));
  } catch (error) {
    console.error('Error fetching transactions:', error);
    throw error;
  }
}