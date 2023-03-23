import { getAuth } from "firebase/auth";
import React from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import firebaseApp from "../firebaseApp";
import "../index.css";
import sendInvoiceRequest from "./sendInvoiceRequest";
import Table from "./Table";
import RecurringOption from "./recurringOption";
import createRecurringInvoice from "./createRecurringInvoice";

const auth = getAuth(firebaseApp);

function toTitleCase(str) {
  return str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}

export default function InvoiceDetailsForm({ setIsLoading }) {
  const navigate = useNavigate();

  const [recipientEmailAddress, setRecipientEmailAddress] = useState("");
  const [paymentId, setPaymentId] = useState("");
  const [issueDate, setIssueDate] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [supplierCompanyName, setSupplierCompanyName] = useState("");
  const [supplierAddressStreet, setSupplierAddressStreet] = useState("");
  const [supplierAddressCity, setSupplierAddressCity] = useState("");
  const [supplierAddressPostalZone, setSupplierAddressPostalZone] =
    useState("");
  const [supplierAddressCountry, setSupplierAddressCountry] = useState("");
  const [customerCompanyName, setCustomerCompanyName] = useState("");
  const [customerAddressStreet, setCustomerAddressStreet] = useState("");
  const [customerAddressCity, setCustomerAddressCity] = useState("");
  const [customerAddressPostalZone, setCustomerAddressPostalZone] =
    useState("");
  const [customerAddressCountry, setCustomerAddressCountry] = useState("");

  const [items, setItems] = useState([]);
  const [recurringOption, setRecurringOption] = useState("notRecurring");

  let formFieldsGeneral = ["recipient email address", "payment id"];
  let formFieldsSupplier = [
    "supplier company name",
    "supplier address street",
    "supplier address city",
    "supplier address postal zone",
    "supplier address country",
  ];
  let formFieldsCustomer = [
    "customer company name",
    "customer address street",
    "customer address city",
    "customer address postal zone",
    "customer address country",
  ];

  let stateKeyValue = {
    recipientEmailAddress: setRecipientEmailAddress,
    paymentId: setPaymentId,
    issueDate: setIssueDate,
    dueDate: setDueDate,
    supplierCompanyName: setSupplierCompanyName,
    supplierAddressStreet: setSupplierAddressStreet,
    supplierAddressCity: setSupplierAddressCity,
    supplierAddressPostalZone: setSupplierAddressPostalZone,
    supplierAddressCountry: setSupplierAddressCountry,
    customerCompanyName: setCustomerCompanyName,
    customerAddressStreet: setCustomerAddressStreet,
    customerAddressCity: setCustomerAddressCity,
    customerAddressPostalZone: setCustomerAddressPostalZone,
    customerAddressCountry: setCustomerAddressCountry,
  };

  function onChangeField(field) {
    function onChange(e) {
      e.preventDefault();
      let fieldFormat = toTitleCase(field);
      fieldFormat = fieldFormat.replace(/\s/g, "");
      fieldFormat = fieldFormat.charAt(0).toLowerCase() + fieldFormat.slice(1);
      stateKeyValue[fieldFormat](e.target.value);
    }
    return onChange;
  }

  function itemToJson(index, item) {
    const itemId = index + 1;
    const itemJson = {
      InvoiceID: itemId,
      InvoiceName: item.itemName,
      InvoiceQuantity: Number(item.quantity),
      InvoiceLineExtension: Number(item.totalPrice),
      // "InvoiceTaxID": "S",
      InvoiceTaxID: 5,
      InvoiceTaxPercent: 10.0,
      InvoiceTaxSchemeID: "GST",
      InvoicePriceAmount: Number(item.price),
      InvoiceBaseQuantity: Number(item.price),
    };

    if (itemId === 1) {
      return itemJson;
    }

    let ret = {};
    for (const key in itemJson) {
      ret[key + itemId.toString()] = itemJson[key];
    }
    return ret;
  }

  function onSubmit(e) {
    e.preventDefault();
    // get user token
    auth.currentUser
      .getIdToken()
      .then((idToken) => {
        // https://stackoverflow.com/questions/18640051/check-if-html-form-values-are-empty-using-javascript
        // show loadingspinner
        setIsLoading(true);
        dispatchAndSendRequest(idToken, recurringOption, getSendInvoiceData())
          .then(({ data }) => {
            setIsLoading(false);
            navigate("/successful", {
              state: data,
            });
          })
          .catch(({ response }) => {
            setIsLoading(false);
            navigate("/unsuccessful", {
              state: response.data,
            });
          });
      })
      .catch((err) => {
        setIsLoading(false);
        // TODO show error message
        navigate("/login");
      });
    return false;
  }

  function dispatchAndSendRequest(idToken, recurringOption, sendInvoiceData) {
    if (recurringOption === "notRecurring") {
      return sendInvoiceRequest(sendInvoiceData, idToken);
    } else {
      return createRecurringInvoice(idToken, recurringOption, sendInvoiceData);
    }
  }

  function getSendInvoiceData() {
    const taxExclusivePrice = items.reduce(
      (accum, { totalPrice }) => accum + Number(totalPrice),
      0
    );
    const taxInclusivePrice = taxExclusivePrice * (1 + 10 / 100);

    return {
      UBLID: 2.1,
      CustomizationID:
        "urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0",
      ProfileID: "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",
      ID: paymentId,
      IssueDate: issueDate,
      DueDate: dueDate,
      InvoiceCode: 380,
      Currency: "AUD",
      AddDocReference: paymentId,

      SupplierStreet: supplierAddressStreet,
      SupplierCity: supplierAddressCity,
      SupplierPost: parseInt(supplierAddressPostalZone),
      SupplierCountry: supplierAddressCountry,
      SupplierRegistration: supplierCompanyName,

      CustomerStreet: customerAddressStreet,
      CustomerCity: customerAddressCity,
      CustomerPost: parseInt(customerAddressPostalZone),
      CustomerCountry: customerAddressCountry,
      CustomerRegistration: customerCompanyName,

      PaymentType: 30, // creditTransfer
      PaymentID: paymentId,
      PaymentTerms: "As agreed",
      TaxAmount: taxInclusivePrice - taxExclusivePrice, // TaxExclusive * 10% (assume GST)
      TaxableAmount: taxExclusivePrice, // TaxExclusiveAmount
      TaxID: "S", // statndard rate (https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL5305/) (assume GST)
      TaxPercent: 10,
      TaxSchemeID: "GST",

      LegalLineExtension: taxExclusivePrice, // TaxExclusiveAmount
      PayableAmount: taxInclusivePrice, // TaxInclusiveAmount
      TaxExclusiveAmount: taxExclusivePrice,
      TaxInclusiveAmount: taxInclusivePrice,

      ...items.reduce(
        (accum, item, i) => ({
          ...accum,
          ...itemToJson(i, item),
        }),
        {}
      ),

      recipient: recipientEmailAddress,
    };
  }

  function fieldToJSX(field) {
    return (
      <td>
        <label key={field}>
          {field}:
          <input
            style={inputAreaStyle}
            required="required"
            type="text"
            onChange={onChangeField(field)}
          />
        </label>
      </td>
    );
  }

  const addGeneralFields = formFieldsGeneral.map(fieldToJSX);

  const addSupplierFields = formFieldsSupplier.map(fieldToJSX);

  const addCustomerFields = formFieldsCustomer.map(fieldToJSX);

  function onDateChange(field) {
    function setDate(e) {
      e.preventDefault();
      stateKeyValue[field](e.target.value);
    }
    return setDate;
  }

  function onRecurringChange(e) {
    e.preventDefault();
    setRecurringOption(e.target.value);
    console.log(recurringOption);
  }

  return (
    <>
      <div
        style={{
          border: "solid",
          padding: "20px",
          borderRadius: "15px",
          borderColor: "rgb(35, 52, 111)",
          backgroundColor: "lightgray",
          marginTop: "6vh",
        }}
      >
        <form id="detailsForm">
          <table>
            <tbody>
              <tr>
                {addGeneralFields}
                <td>
                  <label>issue date:</label>
                  <input
                    style={inputAreaStyle}
                    type="date"
                    onChange={onDateChange("issueDate")}
                  />
                </td>
                <td>
                  <label>due date:</label>
                  <input
                    style={inputAreaStyle}
                    type="date"
                    onChange={onDateChange("dueDate")}
                  />
                </td>
                <td>
                  <RecurringOption
                    style={inputAreaStyle}
                    onChange={onRecurringChange}
                  />
                </td>
              </tr>
              <tr>{addSupplierFields}</tr>
              <tr>{addCustomerFields}</tr>
            </tbody>
          </table>
        </form>
        <Table items={items} setItems={setItems} />
        <button
          type="submit"
          form="detailsForm"
          style={submitButtonStyle}
          onClick={onSubmit}
        >
          Send Invoice
        </button>
      </div>
    </>
  );
}

const inputAreaStyle = {
  borderColor: "black",
  border: "solid",
};

const submitButtonStyle = {
  marginTop: "3vh",
};
