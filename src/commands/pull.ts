import { getTransactions, getAccounts } from '../services/plaid';
import { getAccessToken, hasAccessToken } from '../utils/storage';

interface PullOptions {
  month: string;
  format: string;
}

export async function pullStatements(options: PullOptions) {
  console.log(`Pulling statements for ${options.month} in ${options.format} format...`);
  
  if (!hasAccessToken()) {
    console.error('❌ No linked account found. Please run: npm run dev link');
    console.log('Then complete the linking process and exchange your public token.');
    return;
  }

  const accessToken = getAccessToken()!;
  
  try {
    const [year, month] = options.month.split('-');
    const startDate = `${year}-${month.padStart(2, '0')}-01`;
    const endOfMonth = new Date(parseInt(year), parseInt(month), 0);
    const endDate = `${year}-${month.padStart(2, '0')}-${endOfMonth.getDate().toString().padStart(2, '0')}`;

    console.log(`📊 Fetching transactions from ${startDate} to ${endDate}...`);
    
    const [accounts, transactions] = await Promise.all([
      getAccounts(accessToken),
      getTransactions(accessToken, startDate, endDate)
    ]);

    const totalIncome = transactions
      .filter(tx => tx.amount < 0)
      .reduce((sum, tx) => sum + Math.abs(tx.amount), 0);
    
    const totalExpenses = transactions
      .filter(tx => tx.amount > 0)
      .reduce((sum, tx) => sum + tx.amount, 0);

    const data = {
      month: options.month,
      accounts: accounts.map(acc => ({
        name: acc.name,
        type: acc.type,
        balance: acc.balance.current
      })),
      transactions: transactions.map(tx => ({
        date: tx.date,
        description: tx.name,
        amount: -tx.amount, // Flip sign for intuitive display
        category: tx.category
      })),
      summary: {
        totalIncome: Math.round(totalIncome * 100) / 100,
        totalExpenses: Math.round(totalExpenses * 100) / 100,
        netAmount: Math.round((totalIncome - totalExpenses) * 100) / 100,
        transactionCount: transactions.length
      }
    };

    if (options.format === 'json') {
      console.log(JSON.stringify(data, null, 2));
    } else if (options.format === 'csv') {
      console.log('Date,Description,Amount,Category');
      data.transactions.forEach(tx => {
        console.log(`${tx.date},"${tx.description}",${tx.amount},${tx.category}`);
      });
      console.log(`\n📊 Summary: Income: $${data.summary.totalIncome}, Expenses: $${data.summary.totalExpenses}, Net: $${data.summary.netAmount}`);
    }

    console.log(`\n✅ Found ${transactions.length} transactions for ${options.month}`);
    
  } catch (error) {
    console.error('❌ Failed to pull statements:', error);
    console.log('💡 Make sure your account is still linked. You may need to re-link if the token expired.');
  }
}