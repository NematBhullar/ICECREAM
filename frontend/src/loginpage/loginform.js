import React from "react";
import LogoOnForm from "./logoonform";
import {
  getAuth,
  signInWithEmailAndPassword,
  setPersistence,
  browserSessionPersistence,
} from "firebase/auth";
import firebaseApp from "../firebaseApp";
import { useNavigate } from "react-router-dom";

const auth = getAuth(firebaseApp);

function LoginForm(props) {
  const [user, setUser] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [errMsg, setErrMsg] = React.useState("");

  let navigate = useNavigate();

  function onSubmit(e) {
    e.preventDefault();
    setUser("");
    setPassword("");

    setPersistence(auth, browserSessionPersistence)
      .then(() => {
        // In memory persistence will be applied to the signed in Google user
        // even though the persistence was set to 'none' and a page redirect
        // occurred.
        return signInWithEmailAndPassword(auth, user, password);
      })
      .then(() => {
        navigate("/dashboard");
      })
      .catch((error) => {
        // const errorCode = error.code;
        // const errorMessage = error.message;
        setErrMsg("Invalid Email or Password");
      });
  }

  return (
    <div>
      <form onSubmit={onSubmit}>
        <LogoOnForm />
        <div className="centerElement" style={formStyle}>
          <input
            style={textFormStyle}
            value={user}
            name="login_user"
            onChange={(e) => {
              setUser(e.target.value);
              setErrMsg("");
            }}
            type="text"
            placeholder="Enter Email"
            autoComplete="off"
            required
          />
          <input
            style={textFormStyle}
            name="login_password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setErrMsg("");
            }}
            type="password"
            placeholder="Enter Password"
            required
          />
          <p style={errMsgStyle}>{errMsg}</p>
          <input style={submitFormStyle} type="submit" value="Log in" />
        </div>
      </form>
    </div>
  );
}

const errMsgStyle = {
  textAlign: "center",
  margin: "0px",
  color: "red",
};

const formStyle = {
  backgroundColor: "#F0F0F0",
  textAlign: "center",
  padding: "5vh",
  borderColor: "#27346B",
  border: "solid",
  borderRadius: "20px",
  top: "55vh",
};

const textFormStyle = {
  width: "40vw",
};

const submitFormStyle = {
  marginTop: "10px",
  backgroundColor: "#A2D4BB",
  borderColor: "#A2D4BB",
  width: "15vw",
};

export default LoginForm;
