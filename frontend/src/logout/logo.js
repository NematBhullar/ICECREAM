import React from "react";

function Logo(props) {
  return (
    <div className="centerElement" style={logoDivStyle}>
      <img
        style={logoStyle}
        alt="Ice Cream Logo"
        src="https://t3.ftcdn.net/jpg/04/87/49/88/360_F_487498892_lZgJjiNWuIL9icI7n7cxur70R7tVpMZi.jpg"
      />
    </div>
  );
}

const logoStyle = {
  objectFit: "cover",
  borderRadius: "50vh",
  height: "190px",
  width: "190px",
};

const logoDivStyle = {
  top: "27vh",
};

export default Logo;
