import React from "react";

function Banner(props) {
  return (
    <div style={bannerStyle}>
      <p style={textStyle}>Invoice Failed To Send</p>
    </div>
  );
}

const textStyle = {
  textAlign: "center",
  color: "white",
  fontSize: "40px",
};

const bannerStyle = {
  position: "fixed",
  backgroundColor: "#27346B",
  width: "100vw",
  height: "13vh",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

export default Banner;
