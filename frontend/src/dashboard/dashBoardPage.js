import React from "react";
import "../index.css";
import Banner from "./banner";
import LogoutButton from "./logoutbutton";
import DashboardTitle from "./dashboardtitle";
import CreateInvoice from "./createinvoice";
import ShowInvoice from "./showinvoice";
import { getAuth } from "firebase/auth";
import firebaseApp from "../firebaseApp";
import { Navigate, useNavigate } from "react-router-dom";

const auth = getAuth(firebaseApp);

function DashBoardPage(props) {
  const navigate = useNavigate();
  const user = auth.currentUser;

  if (user === null) {
    console.log("user == null");
    return <Navigate to="/login" />;
  }

  user.getIdToken().catch((err) => {
    console.log("cannot get id token");
    navigate("/login");
  });

  return (
    <div style={dashboardPageStyle}>
      <div style={contentStyle}>
        <Banner />
        <LogoutButton />
        <DashboardTitle />
        <CreateInvoice />
        <ShowInvoice />
      </div>
    </div>
  );
}

const dashboardPageStyle = {
  backgroundImage:
    "url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_rOKxNj3r8CwoWTJvxFQ8R48MiERPLwPrXg&usqp=CAU)",
  width: "100vw",
  height: "100vh",
};

const contentStyle = {
  backgroundColor: "lightgray",
  height: "100vh",
  width: "60vw",
  margin: "auto",
  borderRadius: "15px",
};

export default DashBoardPage;
