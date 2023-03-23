import React from "react";
import "../index.css";

const greeting = "Welcome to IceCream online invoicing!";
const info =
  "Login to continue using our e-invoicing services. Don't have an account? Sign up for free access.";

function Greeting(props) {
  return (
    <div className="centerElement" style={greetingStyle}>
      <h1 style={greetingTextStyle}>{greeting}</h1>
      <p style={infoStyle}> {info} </p>
    </div>
  );
}

const greetingStyle = {
  textAlign: "center",
  top: "50vh",
};

const greetingTextStyle = {
  color: "cornFlowerBlue",
  fontWeight: "700",
  width: "39vw",
};

const infoStyle = {
  width: "39vw",
};

export default Greeting;
