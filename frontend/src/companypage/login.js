import React from "react";
import { useNavigate } from "react-router-dom";
import "../index.css";

function Login(props) {
  let navigate = useNavigate();
  function onClick() {
    navigate("/login");
  }
  return (
    <div className="centerElement" style={loginStyle}>
      <button className="round-button" style={buttonStyle} onClick={onClick}>
        Click To Login
      </button>
    </div>
  );
}

const loginStyle = {
  top: "70vh",
};

const buttonStyle = {
  backgroundColor: "#27346B",
  border: "#27346B",
  width: "159px",
};

export default Login;
