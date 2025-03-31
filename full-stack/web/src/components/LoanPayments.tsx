import React from 'react';
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
      due_date
      loan_payments {
        id
        loan_id
        payment_date
        amount
      }
      payment_status
    }
  }
`;

interface Loan {
  id: number;
  name: string;
  principal: number;
  interest_rate: number;
  due_date: string;
  loan_payments: { id: number; loan_id: number; payment_date: string; amount: number }[];
  payment_status: string;
}

const LoanPayments: React.FC = () => {
  const { loading, error, data } = useQuery(GET_LOANS);

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
      <h1 className="title">Loan Payment Status</h1>
      <div className="loan-list">
        {loans.map((loan) => (
          <LoanCard key={loan.id} loan={loan} />
        ))}
      </div>
    </div>
  );
};

export default LoanPayments;
