import React from "react";
import "../index.css";
import Logo from "./logo";
import SmallTextRedirects from "./smalltextredirects";
import Banner from "./banner";
import DownloadButton from "./DownloadButton";
import DownloadInvoice from "./downloadinvoice";
import Paragraph from "./paragraph";
import { useLocation } from "react-router-dom";

function SuccessfulPage(props) {
  const params = useLocation();
  return (
    <div style={PageStyle}>
      <Banner />
      <Logo />
      <Paragraph />
      <DownloadInvoice invoiceURL={params.state.invoice_url} />
      <DownloadButton reportJson={params.state.report} />
      <SmallTextRedirects />
    </div>
  );
}
const PageStyle = {
  backgroundImage:
    "url(https://media.istockphoto.com/photos/scoop-of-yellow-ice-cream-picture-id480203472?k=20&m=480203472&s=612x612&w=0&h=3huGXkC0dyXomJgzlg_FvvPjZGTjFdMdsC53ra9VTN4=)",
  width: "100vw",
  height: "100vh",
};

export default SuccessfulPage;
