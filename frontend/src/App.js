import CompanyPage from "./companypage/companyPage";
import LoginPage from "./loginpage/loginPage";
import CreateAccountPage from "./createaccount/createAccountPage";
import DashBoardPage from "./dashboard/dashBoardPage";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import UnsuccessfulPage from "./unsuccessful/unsuccessfulpage";
import SuccessfulPage from "./successful/successfulpage";
import LogoutPage from "./logout/logoutpage";
import SendTheInvoicePage from "./sendtheinvoice/sendTheInvoicePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CompanyPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/createaccount" element={<CreateAccountPage />} />
        <Route path="/dashboard" element={<DashBoardPage />} />
        <Route path="/unsuccessful" element={<UnsuccessfulPage />} />
        <Route path="/successful" element={<SuccessfulPage />} />
        <Route path="/logout" element={<LogoutPage />} />
        <Route path="/createinvoice" element={<SendTheInvoicePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
