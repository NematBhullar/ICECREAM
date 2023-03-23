import React from "react";
import "../index.css";

function Banner(props) {
  return (
    <div style={bannerStyle}>
      <h1 style={bannerTextStyle}>Log Out</h1>
    </div>
  );
}

const bannerStyle = {
  position: "fixed",
  backgroundColor: "#27346B",
  width: "100vw",
  height: "13vh",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

const bannerTextStyle = {
  color: "white",
  textAlign: "center",
  fontSize: "40px",
};

export default Banner;
