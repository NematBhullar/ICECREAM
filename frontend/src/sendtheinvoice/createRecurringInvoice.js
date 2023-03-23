import axios from "axios";
import hubUrl from "../config";

function createRecurringInvoice(token, recurringOption, invoiceData) {
  const intervalMap = {
    daily: "D",
    weekly: "W",
    monthly: "M",
    minute: "m",
  };
  const reqHeaders = {
    "Content-Type": "application/json",
    Authorization: "Bearer " + token,
  };

  invoiceData.frequency = "1" + intervalMap[recurringOption];
  return axios
    .post(hubUrl + "/app/recurring_invoices", invoiceData, {
      headers: reqHeaders,
    })
    .then(({ data }) => {
      return {
        data: {
          report: data,
        },
      };
    });
}

export default createRecurringInvoice;
