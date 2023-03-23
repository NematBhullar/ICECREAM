import React from "react";
import "../index.css";

const Heading = "Unsuccessful";
const info =
  "Your invoice was not sucessfully sent to the recipients. Would you like to download the confirmation report?";

function Paragraph(props) {
  return (
    <div className="centerElement" style={HeadingStyle}>
      <h1 style={HeadingTextStyle}>{Heading}</h1>
      <p style={infoStyle}> {info} </p>
    </div>
  );
}

const HeadingStyle = {
  textAlign: "center",
  top: "40vh",
};

const HeadingTextStyle = {
  color: "Black",
  fontWeight: "700",
  width: "39vw",
};

const infoStyle = {
  width: "40vw",
};

export default Paragraph;
