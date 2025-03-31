import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";
import AddPayment from "./components/AddPayment.tsx";
import LoanPayments from "./components/LoanPayments.tsx";
import { LoanCalculator } from "./components/LoanCalculator.tsx";
import Navbar from "./components/Navbar.tsx";

const client = new ApolloClient({
  uri: "http://localhost:2024/graphql",
  cache: new InMemoryCache(),
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ApolloProvider client={client}>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<LoanPayments />} />
          <Route path="/make-payment" element={<AddPayment />} />
          <Route path="/loan-calculator" element={<LoanCalculator />} />
        </Routes>
      </BrowserRouter>
    </ApolloProvider>
  </StrictMode>
);
