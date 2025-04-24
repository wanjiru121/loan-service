import { gql, useQuery } from '@apollo/client';
import LoanCard from './LoanCard';
import '../style/LoanPayment.css';

const GET_LOANS = gql`
  query GetLoans {
    loans {
      id
      name
      principal
      interest_rate
      loan_payments {
        id
        loan_id
        payment_date
        amount
        status
        due_date
      }
      remaining_balance
      expected_repayment_amount
      months
    }
  }
`;

interface Loan {
  id: number;
  name: string;
  principal: number;
  interest_rate: number;
  loan_payments: { id: number; loan_id: number; payment_date: Date; amount: number, status: string, due_date: Date }[];
  remaining_balance: number;
  expected_repayment_amount: number;
  months: number;
}

const LoanPayments = () => {
  const { loading, error, data } = useQuery<{ loans: Loan[] }>(GET_LOANS);

  if (loading) return <p>Loading...</p>;
  if (error) {
    return (
      <div className="error-message">
        <h2>⚠️ Error Loading Loans</h2>
        <p>Something went wrong while fetching loan data. Please try again later.</p>
      </div>
    );
  }

  const loans: Loan[] = data?.loans ?? [];

  return (
    <div className="loan-app">
      <h1 className="title">Loans and Loan Payments</h1>
      <div className="loan-list">
        {loans.map((loan) => (
          <LoanCard key={loan.id} loan={loan} />
        ))}
      </div>
    </div>
  );
};

export default LoanPayments;
