import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App";

const el = document.getElementById("dialogs");

if (el) {
  ReactDOM.render(<App />, el);
}
