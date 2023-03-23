import React from "react";
import { useNavigate } from "react-router-dom";
import "../index.css";

function LogoutButton(props) {
  let navigate = useNavigate();
  function onClick() {
    navigate("/logout");
  }
  return (
    <div style={logoutButtonLocationStyle}>
      <button onClick={onClick} style={logoutButtonStyle}>
        Log Out
      </button>
    </div>
  );
}

const logoutButtonStyle = {
  //backgroundImage:"url(https://icon2.cleanpng.com/20201018/xtq/transparent-web-interface-icons-icon-logout-icon-5f8bbf9bc2f138.8715297616029940757985.jpg)",
  backgroundSize: "100%",
  height: "10vh",
  //width:"10vh",
  backgroundColor: "#23346F",
  border: "transparent",
};

const logoutButtonLocationStyle = {
  position: "absolute",
  top: "1.5vh",
  right: "3vw",
};

export default LogoutButton;
