#!/usr/bin/env node

import { Command } from 'commander';
import { pullStatements } from './commands/pull';
import { linkAccount } from './commands/link';
import { exchangePublicToken } from './services/plaid';
import { saveAccessToken } from './utils/storage';

const program = new Command();

program
  .name('budget-tracker')
  .description('CLI tool for tracking budget and pulling monthly statements')
  .version('1.0.0');

program
  .command('pull')
  .description('Pull monthly statements')
  .option('-m, --month <month>', 'Specific month (YYYY-MM)', new Date().toISOString().slice(0, 7))
  .option('-f, --format <format>', 'Output format (json, csv)', 'json')
  .action(pullStatements);

program
  .command('link')
  .description('Link your RBC bank account')
  .action(linkAccount);

program
  .command('exchange <publicToken>')
  .description('Exchange public token for access token')
  .action(async (publicToken: string) => {
    try {
      console.log('Exchanging public token...');
      const result = await exchangePublicToken(publicToken);
      
      saveAccessToken(result.accessToken, result.itemId);
      
      console.log('✅ Success! Your RBC account is now linked and ready to use.');
      console.log(`Item ID: ${result.itemId}`);
      console.log('\n🎉 You can now pull your statements with: npm run dev pull');
    } catch (error) {
      console.error('❌ Failed to exchange token:', error);
    }
  });

program.parse();