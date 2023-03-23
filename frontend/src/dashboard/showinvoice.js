import React from "react";
import { useState, useEffect } from "react";
import "../index.css";
import {
  getStorage,
  ref as storageRef,
  getDownloadURL,
} from "firebase/storage";
import {
  getDatabase,
  ref,
  set,
  query,
  orderByKey,
  onValue,
  off,
} from "firebase/database";
import firebaseApp from "../firebaseApp";
import { getAuth } from "firebase/auth";
import FindOverdueButton from "./findOverdueButton";
import SelectSearch from "./selectSearch";

const auth = getAuth(firebaseApp);
const db = getDatabase(firebaseApp);
const storage = getStorage(firebaseApp);

export default function ShowInvoice(props) {
  const [invoiceData, setInvoiceData] = useState({}); // all the invoices
  const [viewInvoices, setViewInvoices] = useState({}); // the searched invoices
  const [searchTerm, setSearchTerm] = useState("");
  const [isFindingOverdue, setIsFindingOverdue] = useState(false);
  const [searchOver, setSearchOver] = useState("Invoice Id");

  // called when search bar is updating
  function onChange(e) {
    // This is just the search bar
    e.preventDefault();
    setSearchTerm(e.target.value);
  }

  // called when checkbox is checked
  const onCheck = (invNum) => {
    // On checkbox check, change state of checked to !checked
    let clone = structuredClone(invoiceData);
    clone[invNum].paid = !invoiceData[invNum].paid;
    setInvoiceData(clone);

    updateDatabase(invNum, clone[invNum]);
  };

  function updateDatabase(id, updatedObj) {
    const currUserId = auth.currentUser.uid;
    const invoiceRef = ref(db, "invoices/" + currUserId + "/" + id.toString());
    set(invoiceRef, updatedObj);
  }

  function redirectToDownloadUrl(blobUrl) {
    const blobRef = storageRef(storage, blobUrl);
    getDownloadURL(blobRef)
      .then((url) => {
        window.open(url, "_blank").focus();
      })
      .catch((err) => {
        console.log(err);
      });
  }

  // convert objects to jsx
  const convertObjToLinks = (invNum, invObj) => {
    return (
      // Convert given data to our data
      <div style={anchorDivStyle} key={invNum}>
        <input
          type="checkBox"
          onChange={() => onCheck(invNum)}
          checked={invObj.paid}
        />
        <p style={textStyle} onClick={() => redirectToDownloadUrl(invObj.url)}>
          invoice id: {invObj.payment_id}
          <br></br> issue date: {invObj.issue_date} due date: {invObj.due_date}{" "}
          recipient: {invObj.recipient_email}
        </p>
      </div>
    );
  };

  // update viewInvoices (what the user can see)
  useEffect(() => {
    if (isFindingOverdue) {
      setViewInvoices(
        Object.entries(invoiceData)
          .filter(([key, val]) =>
            filterOverdueAndSearchTerm(
              searchOverMap[searchOver],
              val,
              searchTerm,
              new Date()
            )
          )
          .reduce((obj, [key, val]) => {
            obj[key] = invoiceData[key];
            return obj;
          }, {})
      );
    } else {
      setViewInvoices(
        Object.entries(invoiceData)
          .filter(([key, val]) =>
            doTheFilterToSearch(val[searchOverMap[searchOver]], searchTerm)
          )
          .reduce((obj, [key, val]) => {
            obj[key] = invoiceData[key];
            return obj;
          }, {})
      );
    }
  }, [invoiceData, searchTerm, isFindingOverdue, searchOver]);

  // update invoiceData (all the invoices)
  useEffect(() => {
    const currUserId = auth.currentUser.uid;
    const userInvoicesRef = ref(db, "invoices/" + currUserId);
    const queryRef = query(userInvoicesRef, orderByKey());

    onValue(queryRef, (snapshot) => {
      let tmpData = {};
      snapshot.forEach((childSnapshot) => {
        const invoiceId = childSnapshot.key;
        const invoiceVal = childSnapshot.val();
        tmpData[invoiceId] = invoiceVal;
      });
      setInvoiceData(tmpData);
    });
    return () => off(queryRef);
  }, []);

  return (
    <>
      <FindOverdueButton
        isFindingOverdue={isFindingOverdue}
        setIsFindingOverdue={setIsFindingOverdue}
        overdueInvoicesNum={getOverdueInvoiceNum(
          invoiceData,
          searchTerm,
          searchOverMap[searchOver]
        )}
      />
      <div style={{ padding: "10vh" }}>
        <div>
          <input
            className="centerElement"
            style={searchBarStyle}
            onChange={onChange}
            type="text"
            placeholder={`Search ${searchOver} Here`}
          />
          <SelectSearch searchOver={searchOver} setSearchOver={setSearchOver} />
        </div>
        <div className="centerElement" style={parentDivStyle}>
          <p
            style={{
              textAlign: "center",
              fontWeight: "bold",
              textDecoration: "underline",
            }}
          >
            Check the checkbox to mark invoice as paid
          </p>
          <p
            style={{
              textAlign: "center",
              fontWeight: "bold",
              textDecoration: "underline",
            }}
          >
            Click the box to view the invoice
          </p>
          {(() => {
            let putSearchedListOn = Object.entries(viewInvoices).map(
              ([key, val]) => convertObjToLinks(key, val)
            );
            // indicate there are no invoices
            return putSearchedListOn.length === 0 ? (
              <p
                style={{
                  textAlign: "center",
                  fontWeight: "bold",
                  fontSize: "xx-large",
                }}
              >
                No invoices!
              </p>
            ) : (
              putSearchedListOn
            );
          })()}
        </div>
      </div>
    </>
  );
}

// to search the key that match the term
function doTheFilterToSearch(key, term) {
  return key.toString().toLowerCase().includes(term.toLowerCase());
}

function filterOverdueAndSearchTerm(searchKey, val, term, date) {
  if (val.paid === false && date >= new Date(val.due_date)) {
    return doTheFilterToSearch(val[searchKey], term);
  }
  return false;
}

function getOverdueInvoiceNum(invoiceData, searchTerm, searchKey) {
  return Object.entries(invoiceData).filter(([key, val]) =>
    filterOverdueAndSearchTerm(searchKey, val, searchTerm, new Date())
  ).length;
}

const searchOverMap = {
  "Invoice Id": "payment_id",
  Recipient: "recipient_email",
};

const parentDivStyle = {
  top: "80vh",
  border: "solid",
  height: "38vh",
  width: "50vw",
  overflow: "auto",
  borderRadius: "5px",
  borderColor: "#23346F",
  borderWidth: "4px",
};

const textStyle = {
  fontWeight: "bold",
  paddingLeft: "2rem",
};

const anchorDivStyle = {
  border: "Solid",
  overflow: "auto",
  padding: "1vh",
  borderColor: "#23346F",
};

const searchBarStyle = {
  top: "54vh",
  left: "45vw",
  maxWidth: "45vw",
  border: "solid",
};
