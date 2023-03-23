import React from "react";
import "../index.css";

function LogoOnForm(props) {
  return (
    <div className="centerElement">
      <img
        style={logoStyle}
        alt="Icecream Logo"
        src="https://previews.123rf.com/images/imagestore/imagestore1606/imagestore160601991/58756408-chocolate-ice-cream-scoop-from-top-on-white-background.jpg"
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
