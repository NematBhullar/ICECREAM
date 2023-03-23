import React from "react";
import "../index.css";
import Logo from "./logo";
import SmallTextRedirects from "./smalltextredirects";
import Banner from "./banner";
import DownloadButton from "./DownloadButton";
import Paragraph from "./paragraph";
import { useLocation } from "react-router-dom";

function UnsuccessfulPage(props) {
  const params = useLocation();

  let report = params.state.report;
  if (report === undefined) {
    report = params.state;
  }

  return (
    <div style={PageStyle}>
      <Banner />
      <Logo />
      <Paragraph />
      <DownloadButton reportJson={report} />
      <SmallTextRedirects />
    </div>
  );
}

const PageStyle = {
  backgroundImage:
    "url(https://www.kalscoops.com/wp-content/uploads/2018/02/MintChocChip-SideScoop-480x480.jpg)",
  width: "100vw",
  height: "100vh",
};

export default UnsuccessfulPage;
