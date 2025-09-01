import { getAccountByName, getTransactionsByAccountName } from '../services/plaid';
import { getAccessToken, getCachedTransactions, hasAccessToken } from '../utils/storage';

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

  // TODO: check cache conditional here
  // const cachedTransactions = getCachedTransactions(options.month);
  // if (!cachedTransactions) {
  //   console.error('❌ No cached transactions found for the specified month.');
  //   return;
  // }

  const accessToken = getAccessToken()!;

  try {
    const [year, month] = options.month.split('-');
    const startDate = `${year}-${month.padStart(2, '0')}-01`;
    const endOfMonth = new Date(parseInt(year), parseInt(month), 0);
    const endDate = `${year}-${month.padStart(2, '0')}-${endOfMonth.getDate().toString().padStart(2, '0')}`;

    console.log(`📊 Fetching transactions from ${startDate} to ${endDate}...`);
    
    const [acc, transactions] = await Promise.all([
      getAccountByName('RBC ION+ Visa', accessToken),
      getTransactionsByAccountName('RBC ION+ Visa', accessToken, startDate, endDate)
    ]);

    const totalExpenses = transactions
      .filter(tx => tx.amount > 0)
      .reduce((sum, tx) => sum + tx.amount, 0);

    const data = {
      month: options.month,
      accounts: {
        name: acc.name,
        type: acc.type,
        balance: acc.balance.current
      },
      transactions: transactions.map(tx => ({
        date: tx.date,
        description: tx.name,
        amount: -tx.amount, // Flip sign for intuitive display
        category: tx.category
      })),
      summary: {
        totalExpenses: Math.round(totalExpenses * 100) / 100,
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
    }

    console.log(`\n✅ Found ${transactions.length} transactions for ${options.month}`);
    
  } catch (error) {
    console.error('❌ Failed to pull statements:', error);
    console.log('💡 Make sure your account is still linked. You may need to re-link if the token expired.');
  }
}