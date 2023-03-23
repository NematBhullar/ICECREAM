import Greeting from "./greeting";
import Logo from "./logo";
import Login from "./login";
import CreateAccount from "./createAccount";
import "../index.css";

function CompanyPage(prop) {
  return (
    <div style={companyPageStyle}>
      <div style={createBox}>
        <Greeting />
        <Logo />
        <Login />
        <CreateAccount />
      </div>
    </div>
  );
}

const companyPageStyle = {
  //backgroundColor: "navy",
  width: "100vw",
  minHeight: "100vh",
  display: "flex",
  backgroundImage:
    "url(https://thumbs.dreamstime.com/z/tax-payment-icon-flat-style-budget-invoice-vector-illustration-white-isolated-background-calculate-document-seamless-pattern-188721509.jpg)",
};

const createBox = {
  height: "100vh",
  width: "40vw",
  backgroundColor: "lightGray",
  margin: "auto",
  borderRadius: "20px",
};

export default CompanyPage;
