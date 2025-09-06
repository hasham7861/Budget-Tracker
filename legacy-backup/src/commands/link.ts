import { createLinkToken } from '../services/plaid';

export async function linkAccount() {
  try {
    console.log('Creating link token for RBC connection...');
    
    const { linkToken, hostedLinkUrl } = await createLinkToken();
    
    console.log('\n🔗 Link Token Created Successfully!');
    console.log(`Link Token: ${linkToken}`);
    
    console.log('\n📋 Next Steps:');
    console.log(`1. Go to: ${hostedLinkUrl}`);
    console.log('2. Select "Royal Bank of Canada" from the institution list');
    console.log('3. For SANDBOX testing, use these credentials:');
    console.log('   Username: user_good');
    console.log('   Password: pass_good');
    console.log('4. Complete the linking process');
    console.log('5. Copy the public_token from the success page');
    console.log('6. Use it with: npm run dev exchange <public_token>');
    
  } catch (error) {
    console.error('Failed to create link token:', error);
  }
}