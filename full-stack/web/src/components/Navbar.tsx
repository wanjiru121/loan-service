import { NavLink } from 'react-router-dom';
import '../style/Navbar.css';
import NumidaLogo from '../assets/logo.numida.png'

const Navbar = () => {
  return (
    <nav className="sidebar">
       <div className="logo">
        <img src={NumidaLogo} alt="Numida Logo" />
      </div>
      <ul className="nav-links">
        <li>
          <NavLink to="/" className={({ isActive }) => (isActive ? 'active' : '')}>
            Loan Payments
          </NavLink>
        </li>
        <li>
          <NavLink to="/make-payment" className={({ isActive }) => (isActive ? 'active' : '')}>
            Make Payment
          </NavLink>
        </li>
        <li>
          <NavLink to="/loan-calculator" className={({ isActive }) => (isActive ? 'active' : '')}>
            Loan Calculator
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
