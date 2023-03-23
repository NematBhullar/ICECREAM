import React from "react";
import "../index.css";

const Heading = "Oh no! You're leaving...";
const info = "Are you sure?";

function Paragraph(props) {
  return (
    <div className="centerElement" style={HeadingStyle}>
      <h3 style={HeadingTextStyle}>{Heading}</h3>
      <h5 style={infoStyle}> {info} </h5>
    </div>
  );
}

const HeadingStyle = {
  textAlign: "center",
  top: "42vh",
};

const HeadingTextStyle = {
  color: "Black",
  fontWeight: "700",
  width: "40vw",
};

const infoStyle = {
  width: "40vw",
};

export default Paragraph;
