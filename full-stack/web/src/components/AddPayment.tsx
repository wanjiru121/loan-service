import { useState } from 'react';
import { useMutation, useQuery } from '@apollo/client';
import gql from 'graphql-tag';
import '../style/AddPayment.css';

const MAKE_PAYMENT_MUTATION = gql`
  mutation MakePayment($loan_id: Int!, $payment_date: String!, $amount: Float!) {
    makePayment(loan_id: $loan_id, payment_date: $payment_date, amount: $amount) {
      payment {
        id
        loan_id
        payment_date
        amount
      }
    }
  }
`;

const CHECK_LOAN_STATUS_QUERY = gql`
  query CheckLoanStatus($loan_id: Int!) {
    loan(id: $loan_id) {
      id
      principal
      remaining_balance
    }
  }
`;

const AddNewPayment = () => {
  const [loanId, setLoanId] = useState<string>('');
  const [amount, setAmount] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string>('');

  const paymentDate = new Date().toISOString().split('T')[0];
  const loanIdInt = parseInt(loanId, 10) || 0;

  const { data, loading, error: queryError } = useQuery(CHECK_LOAN_STATUS_QUERY, {
    variables: { loan_id: loanIdInt },
    skip: !loanIdInt,
  });

  const [makePayment] = useMutation(MAKE_PAYMENT_MUTATION);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage('');

    if (!loanId || !amount || parseFloat(amount) <= 0) {
      setError('Please fill in all fields and ensure the amount is greater than zero.');
      return;
    }

    if (queryError) {
      setError('Error fetching loan status.');
      return;
    }

    const loan = data?.loan;
    if (!loan) {
      setError('Loan not found.');
      return;
    }

    const remainingAmount = loan.remaining_balance;
    if (remainingAmount <= 0) {
      setError('This loan has already been fully paid.');
      return;
    }

    if (parseFloat(amount) > remainingAmount) {
      setError(`Payment exceeds the remaining amount of $${remainingAmount.toFixed(2)}`);
      return;
    }

    try {
      await makePayment({
        variables: {
          loan_id: loanIdInt,
          payment_date: paymentDate,
          amount: parseFloat(amount),
        },
      });

      setSuccessMessage('Payment added successfully!');
      setLoanId('');
      setAmount('');
    } catch (mutationError) {
      setError(mutationError.message || 'An error occurred while making the payment.');
    }
  };

  return (
    <div className="add-payment-container">
      <h2 className="form-title">Add New Payment</h2>

      {queryError && <div className="error-message">Error loading loan details.</div>}
      {loading && <div className="loading-message">Loading loan details...</div>}
      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      <form onSubmit={handleSubmit} className="payment-form">
        <div className="form-group">
          <label className="form-label">Payment Loan ID</label>
          <input
            name="loan-id"
            type="number"
            value={loanId}
            onChange={(e) => setLoanId(e.target.value)}
            className="form-input"
            placeholder="Enter Loan ID"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Payment Amount</label>
          <input
            name="payment-amount"
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="form-input"
            placeholder="Enter Payment Amount"
          />
        </div>

        <button type="submit" className="submit-button">
          Add Payment
        </button>
      </form>
    </div>
  );
};

export default AddNewPayment;
