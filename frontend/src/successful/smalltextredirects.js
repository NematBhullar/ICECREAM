import { getAuth } from "@firebase/auth";
import React from "react";
import "../index.css";
import { Link } from "react-router-dom";

function SmallTextRedirects(props) {
  console.log(getAuth().currentUser);
  return (
    <div className="centerElement" style={overallStyle}>
      <Link style={linkStyle} to="/dashboard">
        {" "}
        Would you like to return to your dashboard?{" "}
      </Link>
      <p style={{ margin: "10px" }}></p>
    </div>
  );
}

const overallStyle = {
  textAlign: "center",
  top: "80vh",
  borderColor: "black",
};

const linkStyle = {
  color: "#27346B",
  textAlign: "center",
};

export default SmallTextRedirects;
