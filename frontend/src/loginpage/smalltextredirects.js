import React from "react";
import "../index.css";

function SmallTextRedirects(props) {
  return (
    <div className="centerElement" style={overallStyle}>
      <a style={linkStyle} href="/createaccount">
        Want to create an account?
      </a>
      <p style={{ margin: "10px" }}></p>
      <a style={linkStyle} href="/">
        Take me Home, country roads
      </a>
    </div>
  );
}

const overallStyle = {
  textAlign: "center",
  top: "90vh",
  borderColor: "black",
  border: "solid",
  borderRadius: "10px",
  padding: "1vh",
};

const linkStyle = {
  color: "#27346B",
  textAlign: "center",
};

export default SmallTextRedirects;
