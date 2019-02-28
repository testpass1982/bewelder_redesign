import React from "react";
import ReactDOM from "react-dom";
import App from "./containers/App";
import { createStore } from "redux";
import { Provider } from "react-redux";
import reducer from "./reducers";
import api from "./utils/api";
import * as status from "./constants/status";

const el = document.getElementById("dialogs");
api.init();

$("#dialogs-modal").on("show.bs.modal", function(event) {
  console.log("start dialogs main");
  const opponent = $(event.relatedTarget).data("opponent");
  if (el) {
    const initStore = {
      status: status.DIALOG_LIST,
      dialogSet: [],
      dialog: {},
      loading: false
    };
    if (opponent) {
      initStore.status = status.DIALOG_CREATE;
      initStore.opponentId = opponent;
    }
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
