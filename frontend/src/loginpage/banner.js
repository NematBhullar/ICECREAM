import React from "react";
import "../index.css";

function Banner(props) {
  return (
    <div style={bannerStyle}>
      <h1 style={bannerTextStyle}>Log In</h1>
    </div>
  );
}

const bannerStyle = {
  position: "fixed",
  backgroundColor: "#27346B",
  width: "100vw",
  padding: "5vh",
};

const bannerTextStyle = {
  color: "white",
  textAlign: "center",
  fontSize: "40px",
};

export default Banner;
