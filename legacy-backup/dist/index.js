#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const pull_1 = require("./commands/pull");
const program = new commander_1.Command();
program
    .name('budget-tracker')
    .description('CLI tool for tracking budget and pulling monthly statements')
    .version('1.0.0');
program
    .command('pull')
    .description('Pull monthly statements')
    .option('-m, --month <month>', 'Specific month (YYYY-MM)', new Date().toISOString().slice(0, 7))
    .option('-f, --format <format>', 'Output format (json, csv)', 'json')
    .action(pull_1.pullStatements);
program.parse();
//# sourceMappingURL=index.js.map