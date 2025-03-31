import React from 'react';
import { formatDate } from '../utils/formatDate';

interface Loan {
  id: number;
  name: string;
  principal: number;
  interest_rate: number;
  due_date: string;
  loan_payments: { id: number; loan_id: number; payment_date: string; amount: number }[];
  payment_status: string;
}

interface LoanCardProps {
  loan: Loan;
}

const LoanCard: React.FC<LoanCardProps> = ({ loan }) => (
  <div className="loan-card">
    <div className="loan-header">
      <span
        className={`status-badge ${loan.payment_status.toLowerCase().replace(/\s+/g, '-')}`}
      >
        {loan.payment_status.toLowerCase()}
      </span>
    </div>
    <div className="loan-body">
      <h2 className="loan-name">{loan.name}</h2>
      <p>
        <strong>Principal:</strong>{' '}
        <span className="highlight">KSh {loan.principal}</span>
      </p>
      <p>
        <strong>Interest Rate:</strong> {loan.interest_rate}%
      </p>
      <p>
        <strong>Due Date:</strong> {formatDate(loan.due_date)}
      </p>
    </div>
    <div className="loan-footer">
      <strong>Payments:</strong>
      <br />
      <div className="payment-header">
        <span className="header-item">Amount</span>
        <span className="header-item">Payment Date</span>
      </div>
      {loan.loan_payments.length > 0 ? (
        <ul className="payments">
          {loan.loan_payments.map((payment) => (
            <li key={payment.id} className="payment-item">
              <span className="payment-amount">{payment.amount}</span>
              <span className="payment-date">{formatDate(payment.payment_date)}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="no-payment">❌ No payments made yet.</p>
      )}
    </div>
  </div>
);

export default LoanCard;
