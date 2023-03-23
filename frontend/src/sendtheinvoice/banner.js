import React from "react";

export default function Banner(props) {
  return (
    <div style={bannerStyle}>
      <p style={textStyle}>Send Your Invoice!</p>
    </div>
  );
}

const bannerStyle = {
  width: "100vw",
  height: "13vh",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: "#23346F",
};

const textStyle = {
  fontSize: "5vh",
  color: "white",
};
