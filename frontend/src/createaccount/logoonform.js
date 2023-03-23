import React from "react";
import "../index.css";

function LogoOnForm(props) {
  return (
    <div className="centerElement">
      <img
        style={logoStyle}
        alt="Icecream Logo"
        src="https://previews.123rf.com/images/imagestore/imagestore1411/imagestore141100102/33771748-scoop-of-vanilla-ice-cream-on-white-background-with-clipping-path.jpg"
      />
    </div>
  );
}

const logoStyle = {
  position: "relative",
  objectFit: "cover",
  borderRadius: "50vh",
  height: "20vh",
  width: "20vh",
  top: "-13vh",
  border: "solid",
};

export default LogoOnForm;
