import React from "react";

function Logo(props) {
  return (
    <div className="centerElement" style={logoDivStyle}>
      <img
        style={logoStyle}
        alt="Ice Cream Logo"
        src="https://cdn.pixabay.com/photo/2012/04/12/13/15/red-29985_960_720.png"
      />
    </div>
  );
}

const logoStyle = {
  objectFit: "cover",
  borderRadius: "50vh",
  height: "200px",
  width: "200px",
};

const logoDivStyle = {
  top: "25vh",
};

export default Logo;
