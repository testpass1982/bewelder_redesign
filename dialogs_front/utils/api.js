import axios from "axios";
import Cookies from "js-cookie";

let api;
const baseMessagingURL = "/api/messaging";
const dialogsURL = "/dialogs";
const getData = res => res.data;

const requests = {
  get: url => api.get(url).then(getData),
  post: (url, body) => api.post(url, body).then(getData)
};

const dialogs = {
  get: id => requests.get(dialogsURL + (id ? `/${id}` : "")),
  create: (oppId, vacancyId, theme, text) =>
    requests.post("", { oppId, vacancyId, theme, text }),
  sendMessage: (dialogId, text) =>
    requests.post(`${dialogsURL}/${dialogId}/`, { text })
};

function init(baseURL = baseMessagingURL) {
  const csrftoken = Cookies.get("csrftoken");
  api = axios.create({
    baseURL,
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": csrftoken,
      Accept: "application/json",
      "Content-Type": "application/json"
    }
  });
}

export default { init, dialogs };
