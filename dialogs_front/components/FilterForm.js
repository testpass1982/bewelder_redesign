import React from "react";

const FilterForm = ({ value, onFilterChange }) => (
  <div className="form-group">
    <input
      type="text"
      className="form-control pr-4"
      placeholder="Искать переписку"
      value={value}
      onChange={onFilterChange}
    />
    <i
      className="fa fa-search text-success"
      style={{ float: "right", margin: "-28px 10px" }}
    />
  </div>
);

export default FilterForm;
