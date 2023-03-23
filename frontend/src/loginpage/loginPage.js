import React from "react";
import "../index.css";
import Banner from "./banner";
import LoginForm from "./loginform";
import SmallTextRedirects from "./smalltextredirects";

function LoginPage(props) {
  return (
    <div>
      <div>
        <Banner />
        <LoginForm />
        <SmallTextRedirects />
      </div>
    </div>
  );
}

export default LoginPage;
