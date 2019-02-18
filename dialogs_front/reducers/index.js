import {
  TO_DIALOG_VIEW,
  TO_DIALOG_LIST,
  TO_DIALOG_CREATE
} from "../constants/actionTypes";
import * as status from "../constants/status";

export default (state = {}, action) => {
  switch (action.type) {
    case TO_DIALOG_CREATE:
      return {
        ...state,
        status: status.DIALOG_CREATE,
        opponent_id: action.opponent_id
      };
    case TO_DIALOG_VIEW:
      return {
        ...state,
        status: status.DIALOG_VIEW,
        dialog_id: action.dialog_id
      };
    case TO_DIALOG_LIST:
      return {
        ...state,
        status: status.DIALOG_LIST
      };
    default:
      return state;
  }
};
