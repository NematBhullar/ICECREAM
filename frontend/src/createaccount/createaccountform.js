import React from "react";
import LogoOnForm from "./logoonform";
import firebaseApp from "../firebaseApp";
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
import { useNavigate } from "react-router-dom";

const auth = getAuth(firebaseApp);

function LoginForm(props) {
  const [email, setUser] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [errMsg, setErrMsg] = React.useState("");

  let navigate = useNavigate();

  function onSubmit(e) {
    e.preventDefault();
    console.log(email, password);
    setUser("");
    setPassword("");

    createUserWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        // Signed in
        navigate("/dashboard");
      })
      .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.log(errorCode, errorMessage);
        // TODO print error message
        setErrMsg(
          "Password should be at least 6 characters and Email must be valid"
        );
      });
  }

  return (
    <div>
      <form onSubmit={onSubmit}>
        <LogoOnForm />
        <div className="centerElement" style={formStyle}>
          <input
            style={textFormStyle}
            name="login_user"
            value={email}
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
          <input style={submitFormStyle} type="submit" value="Create Account" />
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
  width: "auto",
  textAlign: "center",
};

export default LoginForm;
