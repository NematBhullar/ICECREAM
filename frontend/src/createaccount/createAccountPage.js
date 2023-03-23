import React from "react";
import Banner from "./banner";
import FooterRedirects from "./footerredirects";
import CreateAccountForm from "./createaccountform";

function CreateAccountPage(props) {
  return (
    <div>
      <Banner />
      <CreateAccountForm />
      <FooterRedirects />
    </div>
  );
}

export default CreateAccountPage;
