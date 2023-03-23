import React from "react";
import { useNavigate } from "react-router-dom";
import "../index.css";

function CreateAccount(props) {
  let navigate = useNavigate();
  function onClick() {
    navigate("/createaccount");
  }
  return (
    <div className="centerElement" style={createAccountStyle}>
      <button className="round-button" style={buttonStyle} onClick={onClick}>
        Create Account
      </button>
    </div>
  );
}

const createAccountStyle = {
  top: "80vh",
};

const buttonStyle = {
  backgroundColor: "#A2D4BB",
  borderColor: "#A2D4BB",
};

export default CreateAccount;
