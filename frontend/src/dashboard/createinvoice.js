import React from "react";
import { useNavigate } from "react-router-dom";
import "../index.css";

function CreateInvoice(props) {
  let navigate = useNavigate();
  function onClick() {
    navigate("/createinvoice");
  }
  return (
    <div className="centerElement" style={buttonLocation}>
      <button style={buttonStyle} className="round-button" onClick={onClick}>
        Create And Send A New Invoice
      </button>
    </div>
  );
}

const buttonStyle = {
  backgroundColor: "#3A3E4B",
  borderColor: "#3A3E4B",
};

const buttonLocation = {
  top: "40vh",
};

export default CreateInvoice;
