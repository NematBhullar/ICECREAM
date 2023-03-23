import React from "react";
import "../index.css";
import { getStorage, ref, getDownloadURL } from "firebase/storage";
import firebaseApp from "../firebaseApp";
import download from "./downloadFunc";

const storage = getStorage(firebaseApp);

function DownloadInvoice({ invoiceURL }) {
  function onClick() {
    getDownloadURL(ref(storage, invoiceURL))
      .then((url) => {
        console.log("download " + url);
        download(url, "invoice.xml");
      })
      .catch((err) => {
        console.log(err);
      });
  }
  if (invoiceURL === undefined) {
    return <></>;
  }
  return (
    <div className="centerElement" style={loginStyle}>
      <button className="round-button" style={buttonStyle} onClick={onClick}>
        View Invoice
      </button>
    </div>
  );
}

const loginStyle = {
  top: "70vh",
};

const buttonStyle = {
  backgroundColor: "#27346B",
  border: "#27346B",
  width: "300x",
};

export default DownloadInvoice;
