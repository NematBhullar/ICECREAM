function FindOverdueButton({
  isFindingOverdue,
  setIsFindingOverdue,
  overdueInvoicesNum,
}) {
  function switchIsFindingOverdue() {
    setIsFindingOverdue(!isFindingOverdue);
  }

  return (
    <div className="centerElement" style={buttonLocation}>
      <button
        style={isFindingOverdue ? onButtonStyle : offButtonStyle}
        className="round-button"
        onClick={switchIsFindingOverdue}
      >
        {isFindingOverdue ? "Show all invoices" : "Find all overdue invoices"}
      </button>
      {isFindingOverdue ? (
        <></>
      ) : (
        <span className="bagde" style={badgeStyle}>
          {overdueInvoicesNum}
        </span>
      )}
    </div>
  );
}

const offButtonStyle = {
  backgroundColor: "red",
  borderColor: "red",
};

const onButtonStyle = {
  backgroundColor: "green",
  borderColor: "green",
};

const buttonLocation = {
  top: "47vh",
};

const badgeStyle = {
  position: "absolute",
  top: "-12px",
  right: "-15px",
  padding: "5px 12px",
  borderRadius: "50%",
  background: "black",
  color: "white",
};

export default FindOverdueButton;
