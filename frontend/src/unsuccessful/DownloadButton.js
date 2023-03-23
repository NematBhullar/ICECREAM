import React from "react";
import "../index.css";
import donwloadJson from "../successful/downloadJson";

function DownloadButton({ reportJson }) {
  function onClick() {
    donwloadJson(reportJson, "report.json");
  }
  return (
    <div
      className="centerElement"
      style={{ ...buttonStyle, ...buttonLocation }}
    >
      <button style={buttonStyle} className="round-button" onClick={onClick}>
        Download Confirmation Report
      </button>
    </div>
  );
}

const buttonStyle = {
  backgroundColor: "#3A3E4B",
  borderColor: "#3A3E4B",
};

const buttonLocation = {
  top: "52vh",
};

export default DownloadButton;
