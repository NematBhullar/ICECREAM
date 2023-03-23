import React from "react";
import "../index.css";
import Banner from "./banner";
import Confirm from "./confirm";
import NoButton from "./NoButton";
import Logo from "./logo";
import Paragraph from "./paragraph";

function LogoutPage(props) {
  return (
    <div style={LogoutPageStyle}>
      <Banner />
      <Logo />
      <Paragraph />
      <Confirm />
      <NoButton />
    </div>
  );
}

const LogoutPageStyle = {
  backgroundImage:
    "url(https://www.kindpng.com/picc/m/266-2668611_oreo-cookies-and-cream-ice-cream-scooped-cookies.png)",
  width: "100vw",
  height: "100vh",
};

export default LogoutPage;
