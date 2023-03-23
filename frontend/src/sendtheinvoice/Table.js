import React, { useState, Fragment } from "react";
import { nanoid } from "nanoid";
import ReadOnlyRow from "./ReadOnlyRow";
import EditableRow from "./EditableRow";

const Table = ({ items, setItems }) => {
  const [addFormData, setAddFormData] = useState({
    itemName: "",
    price: "",
    quantity: "",
  });

  const [editFormData, setEditFormData] = useState({
    itemName: "",
    price: "",
    quantity: "",
  });

  const [editItemId, setEditItemId] = useState(null);

  const handleAddFormChange = (event) => {
    event.preventDefault();

    const fieldName = event.target.getAttribute("name");
    const fieldValue = event.target.value;

    const newFormData = { ...addFormData };
    newFormData[fieldName] = fieldValue;

    setAddFormData(newFormData);
  };

  const handleEditFormChange = (event) => {
    event.preventDefault();

    const fieldName = event.target.getAttribute("name");
    const fieldValue = event.target.value;

    const newFormData = { ...editFormData };
    newFormData[fieldName] = fieldValue;

    setEditFormData(newFormData);
  };

  const handleAddFormSubmit = (event) => {
    event.preventDefault();

    const newItem = {
      id: nanoid(),
      itemName: addFormData.itemName,
      price: addFormData.price,
      quantity: addFormData.quantity,
      totalPrice: addFormData.price * addFormData.quantity,
    };

    const newItems = [...items, newItem];
    setItems(newItems);
    setAddFormData({
      itemName: "",
      price: "",
      quantity: "",
    });
  };

  const handleEditFormSubmit = (event) => {
    event.preventDefault();

    const editedItem = {
      id: editItemId,
      itemName: editFormData.itemName,
      price: editFormData.price,
      quantity: editFormData.quantity,
      totalPrice: editFormData.price * editFormData.quantity,
    };

    const newItems = [...items];

    const index = items.findIndex((item) => item.id === editItemId);

    newItems[index] = editedItem;

    setItems(newItems);
    setEditItemId(null);
  };

  const handleEditClick = (event, item) => {
    event.preventDefault();
    setEditItemId(item.id);

    const formValues = {
      itemName: item.itemName,
      price: item.price,
      quantity: item.quantity,
      totalPrice: item.totalPrice,
    };

    setEditFormData(formValues);
  };

  const handleCancelClick = () => {
    setEditItemId(null);
  };

  const handleDeleteClick = (itemId) => {
    const newItems = [...items];

    const index = items.findIndex((item) => item.id === itemId);

    newItems.splice(index, 1);

    setItems(newItems);
  };

  return (
    <div className="app-container">
      <form onSubmit={handleEditFormSubmit}>
        <table>
          <thead>
            <tr>
              <th>Item Name</th>
              <th>Price per quantity</th>
              <th>Quantity</th>
              <th>Total Price</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <Fragment key={item.id}>
                {editItemId === item.id ? (
                  <EditableRow
                    editFormData={editFormData}
                    handleEditFormChange={handleEditFormChange}
                    handleCancelClick={handleCancelClick}
                  />
                ) : (
                  <ReadOnlyRow
                    item={item}
                    handleEditClick={handleEditClick}
                    handleDeleteClick={handleDeleteClick}
                  />
                )}
              </Fragment>
            ))}
          </tbody>
        </table>
      </form>

      <h2>Add an Item</h2>
      <form onSubmit={handleAddFormSubmit}>
        <input
          type="text"
          name="itemName"
          required="required"
          placeholder="Enter item name..."
          value={addFormData.itemName}
          onChange={handleAddFormChange}
        />
        <input
          type="number"
          name="price"
          min="0"
          step="any"
          required="required"
          placeholder="Enter price per quantity..."
          value={addFormData.price}
          onChange={handleAddFormChange}
        />
        <input
          type="number"
          min="1"
          name="quantity"
          required="required"
          placeholder="Enter quantity..."
          value={addFormData.quantity}
          onChange={handleAddFormChange}
        />
        <button type="submit">Add</button>
      </form>
    </div>
  );
};

export default Table;
