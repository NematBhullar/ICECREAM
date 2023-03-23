import React from "react";
import "../index.css";
import donwloadJson from "./downloadJson";

function DownloadButton({ reportJson }) {
  function onClick() {
    donwloadJson(reportJson, "report.json");
  }
  return (
    <div className="centerElement" style={loginStyle}>
      <button style={buttonStyle} className="round-button" onClick={onClick}>
        Download Confirmation Report
      </button>
    </div>
  );
}

const loginStyle = {
  top: "60vh",
};

const buttonStyle = {
  backgroundColor: "#FFFFFF",
  borderColor: "#000080",
  color: "#000080",
};

export default DownloadButton;
