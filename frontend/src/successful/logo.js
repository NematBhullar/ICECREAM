import React from "react";

function Logo(props) {
  return (
    <div className="centerElement" style={logoDivStyle}>
      <img
        style={logoStyle}
        alt="Ice Cream Logo"
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Checkmark_green.svg/1200px-Checkmark_green.svg.png"
      />
    </div>
  );
}

const logoStyle = {
  objectFit: "cover",
  borderRadius: "50vh",
  height: "230px",
  width: "230px",
};

const logoDivStyle = {
  top: "25vh",
};

export default Logo;
