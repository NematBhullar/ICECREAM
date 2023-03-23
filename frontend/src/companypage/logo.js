import React from "react";

function Logo(props) {
  return (
    <div className="centerElement" style={logoDivStyle}>
      <img
        style={logoStyle}
        alt="Ice Cream Logo"
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Strawberry_ice_cream_cone_%285076899310%29.jpg/360px-Strawberry_ice_cream_cone_%285076899310%29.jpg"
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
  top: "20vh",
};

export default Logo;
