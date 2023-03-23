import axios from "axios";
import hubUrl from "../config";

const sendInvoiceRequest = (invoiceObj, token) => {
  const reqHeaders = {
    "Content-Type": "application/json",
    Authorization: "Bearer " + token,
  };
  return axios.post(hubUrl + "/app/send_invoice", invoiceObj, {
    headers: reqHeaders,
  });
};

export default sendInvoiceRequest;
