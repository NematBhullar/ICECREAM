import React from "react";
import "../index.css";

const Heading = "Successful";
const info =
  "Your invoice was sucessfully sent to the recipients. Would you like to download the invoice or confirmation report?";

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
  top: "42vh",
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
