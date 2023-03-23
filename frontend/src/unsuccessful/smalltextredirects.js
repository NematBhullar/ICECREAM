import React from "react";
import { Link } from "react-router-dom";
import "../index.css";

function SmallTextRedirects(props) {
  return (
    <div className="centerElement" style={overallStyle}>
      <Link style={linkStyle} to="/createinvoice">
        Would you like to go back and edit your invoice?
      </Link>
      <p style={{ margin: "1px" }}></p>
    </div>
  );
}

const overallStyle = {
  textAlign: "center",
  top: "57vh",
  borderColor: "black",
};

const linkStyle = {
  color: "#27346B",
  textAlign: "center",
};

export default SmallTextRedirects;
