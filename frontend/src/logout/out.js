import React from "react";
import { useNavigate } from "react-router-dom";
import "../index.css";
import styled from "styled-components";

const Button = styled.button`
  background-color: blue;
  color: white;
  padding: 5px 15px;
  border-radius: 5px;
  outline: 0;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0px 2px 2px lightgray;
`;

function Out(props) {
  let navigate = useNavigate();
  function onClick() {
    navigate("/createaccount");
  }
  return (
    <div className="centerElement" style={logOutStyle}>
      <button className="round-button" style={buttonStyle} onClick={onClick}>
        Yes, Log Out
      </button>
    </div>
  );
}

const logOutStyle = {
  top: "80vh",
};

const buttonStyle = {
  backgroundColor: "#A2D4BB",
  borderColor: "#A2D4BB",
};

export default Out;
