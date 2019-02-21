import React from "react";
import ReactDOM from "react-dom";
import App from "./containers/App";
import { createStore } from "redux";
import { Provider } from "react-redux";
import reducer from "./reducers";
import api from "./utils/api";

const el = document.getElementById("dialogs");
api.init();

$("#dialogs-modal").on("show.bs.modal", function() {
  console.log("start dialogs main");
  if (el) {
    const initStore = {
      dialogs: [],
      dialog: {}
    };
    const store = createStore(reducer, initStore);
    ReactDOM.render(
      <Provider store={store}>
        <App />
      </Provider>,
      el
    );
  }
});

$("#dialogs-modal").on("hidden.bs.modal", function() {
  console.log("close dialgs main");
  ReactDOM.unmountComponentAtNode(el);
});
