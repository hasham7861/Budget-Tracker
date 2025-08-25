#!/usr/bin/env node

import { Command } from 'commander';
import { pullStatements } from './commands/pull';

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

program.parse();