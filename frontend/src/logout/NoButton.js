import React from "react";
import { useNavigate } from "react-router-dom";
import "../index.css";

function NoButton(props) {
  let navigate = useNavigate();
  function onClick() {
    navigate("/dashboard");
  }
  return (
    <div className="centerElement" style={loginStyle}>
      <button style={buttonStyle} className="round-button" onClick={onClick}>
        No, return to dashboard
      </button>
    </div>
  );
}

const loginStyle = {
  top: "58vh",
};

const buttonStyle = {
  backgroundColor: "#FFFFFF",
  borderColor: "#000080",
  color: "#000080",
};

export default NoButton;
