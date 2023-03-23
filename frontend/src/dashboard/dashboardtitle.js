import React from "react";
import "../index.css";

function DashboardTitle(props) {
  return (
    <div className="centerElement" style={locationTextStyle}>
      <h1 style={largeTextStyle}>Dashboard</h1>
    </div>
  );
}

const locationTextStyle = {
  top: "25vh",
};

const largeTextStyle = {
  fontWeight: "bold",
  fontSize: "4vw",
  border: "solid",
  borderRadius: "10px",
  padding: "3vh",
  color: "#3A3E4B",
};

export default DashboardTitle;
