import { useEffect, useState } from "react";
import "../style/LoanCalculator.css";

export const LoanCalculator = () => {
  const [principal, setPrincipal] = useState("");
  const [rate, setRate] = useState("");
  const [months, setMonths] = useState("");
  const [interest, setInterest] = useState(0);
  const [totalPayment, setTotalPayment] = useState(0);

  useEffect(() => {
    const p = parseFloat(principal);
    const r = parseFloat(rate);
    const m = parseFloat(months);

    if (p > 0 && r > 0 && m > 0) {
      const calculatedInterest = (p * r * m) / 100;
      setInterest(calculatedInterest);
      setTotalPayment(p + calculatedInterest);
    } else {
      setInterest(0);
      setTotalPayment(0);
    }
  }, [principal, rate, months]);

  return (
    <div className="calculator-container">
      <h2 className="calculator-title">Loan Calculator</h2>

      <div className="input-group">
        <label>Principal Amount</label>
        <input
          type="number"
          value={principal}
          onChange={(e) => setPrincipal(e.target.value)}
          className="input-field"
          placeholder="Enter Principal Amount"
          min="1"
        />
      </div>

      <div className="input-group">
        <label>Interest Rate (%)</label>
        <input
          type="number"
          value={rate}
          onChange={(e) => setRate(e.target.value)}
          className="input-field"
          placeholder="Enter Interest Rate"
          min="1"
        />
      </div>

      <div className="input-group">
        <label>Loan Duration (Months)</label>
        <input
          type="number"
          value={months}
          onChange={(e) => setMonths(e.target.value)}
          className="input-field"
          placeholder="Enter Loan Duration"
          min="1"
        />
      </div>

      <div className="result">
        {interest > 0 ? (
          <>
            <h3>
              Total Interest:{" "}
              <span className="interest-amount">{interest.toFixed(2)}</span>
            </h3>
            <h3>
              Total Payment:{" "}
              <span className="total-amount">{totalPayment.toFixed(2)}</span>
            </h3>
          </>
        ) : (
          <h3 className="placeholder-text">🔹 Enter values to calculate.</h3>
        )}
      </div>
    </div>
  );
};
