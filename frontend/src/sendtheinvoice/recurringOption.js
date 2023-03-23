export default function RecurringOption({ onChange, style }) {
  return (
    <div>
      <label>recurring option:</label>
      <select style={style} name="recurringOption" required onChange={onChange}>
        <option value="notRecurring">Not Recurring</option>
        <option value="daily">Daily</option>
        <option value="weekly">Weekly</option>
        <option value="monthly">Monthly</option>
        <option value="minute">Per minute</option>
      </select>
    </div>
  );
}
