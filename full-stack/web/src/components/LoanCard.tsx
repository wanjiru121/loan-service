import { formatDate } from '../utils/formatDate';

interface LoanPayment {
  id: number;
  loan_id: number;
  payment_date: string;
  amount: number;
  status: string;
  due_date: string;
}

interface Loan {
  id: number;
  name: string;
  principal: number;
  interest_rate: number;
  remaining_balance: number;
  expected_repayment_amount: number;
  months: number;
  loan_payments: LoanPayment[];
}

interface LoanCardProps {
  loan: Loan;
}

const LoanCard = ({ loan }: LoanCardProps) => (
  <div className="loan-card">
    <div className="loan-body">
      <h2 className="loan-name">{loan.name}</h2>
      <p>
        <strong>Principal:</strong>{' '}
        <span className="highlight">KSh {loan.principal}</span>
      </p>
      <p>
        <strong>Total Repayment:</strong>{' '}
        <span className="highlight">{loan.expected_repayment_amount}</span>
      </p>
      <p>
        <strong>Interest Rate:</strong> {loan.interest_rate}%
      </p>
      <p>
        <strong>Months:</strong> {loan.months}
      </p>
      <p>
        <strong>Remaining Balance:</strong> {loan.remaining_balance}
      </p>
    </div>

    <div className="loan-footer">
      <strong>Payments:</strong>
      <br />
      <div className="payment-header">
        <span className="header-item">Amount</span>
        <span className="header-item">Payment Date</span>
        <span className="header-item">Due Date</span>
        <span className="header-item">Status</span>
      </div>

      {loan.loan_payments.length > 0 ? (
        <ul className="payments">
          {loan.loan_payments.map((payment) => (
            <li key={payment.id} className="payment-item">
              <span className="payment-amount">KSh {payment.amount}</span>
              <span className="payment-and-due-date">{formatDate(payment.payment_date)}</span>
              <span className="payment-and-due-date">{formatDate(payment.due_date)}</span>
              <span className={`status-badge ${payment.status.toLowerCase().replace(/\s+/g, '-')}`}>
                {payment.status}
              </span>
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
