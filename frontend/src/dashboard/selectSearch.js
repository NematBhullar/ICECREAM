function SelectSearch({ searchOver, setSearchOver }) {
  function updateSearchOver(e) {
    setSearchOver(e.target.value);
  }

  return (
    <div style={selectStyle}>
      <select
        name="search"
        id="search-select"
        value={searchOver}
        onChange={updateSearchOver}
      >
        {/* <option value="">--Please choose an option--</option> */}
        <option value="Invoice Id">invoice id</option>
        <option value="Recipient">recipient</option>
        {/* <option value="due date">due date</option>
            <option value="issue date">issue date</option> */}
      </select>
    </div>
  );
}

const selectStyle = {
  position: "fixed",
  top: "51.5vh",
  right: "22vw",
  width: "10vw",
};

export default SelectSearch;
