import React, { useState } from "react";
import Banner from "./banner";
import InvoiceDetailsForm from "./invoicedetailsform";
import LogoutButton from "../dashboard/logoutbutton";
import LoadingOverlay from "@ronchalant/react-loading-overlay";
import SecretMessage from "./secretmessage";

export default function SendTheInvoicePage(props) {
  const [isLoading, setIsLoading] = useState(false);
  return (
    <LoadingOverlay active={isLoading} spinner text="sending your invoice">
      <div style={backgroundStyle}>
        <div style={pageStyle}>
          <Banner />
          <InvoiceDetailsForm setIsLoading={setIsLoading} />
          <LogoutButton />
          <SecretMessage />
        </div>
      </div>
    </LoadingOverlay>
  );
}

const pageStyle = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  spaceBetween: "20px",
  alignItems: "center",
  flexWrap: "wrap",
};

const backgroundStyle = {
  backgroundImage:
    "url(https://i.pinimg.com/originals/8e/53/45/8e53458e21512ed515fa6e626efe7c96.jpg)",
  height: "200vh",
  width: "100vw",
};
