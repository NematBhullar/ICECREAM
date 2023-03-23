import { getAuth, signOut } from "firebase/auth";
import React from "react";
import { useNavigate } from "react-router-dom";
import firebaseApp from "../firebaseApp";
import "../index.css";

const auth = getAuth(firebaseApp);

function Confirm(props) {
  let navigate = useNavigate();
  function onClick() {
    signOut(auth).then(navigate("/")).catch(navigate("/"));
  }
  return (
    <div className="centerElement" style={loginStyle}>
      <button className="round-button" style={buttonStyle} onClick={onClick}>
        Yes, continue to exit
      </button>
    </div>
  );
}

const loginStyle = {
  top: "53vh",
};

const buttonStyle = {
  backgroundColor: "#27346B",
  border: "#27346B",
  width: "300x",
};

export default Confirm;
