import * as types from "../constants/actionTypes";
import * as status from "../constants/status";

export default (state = {}, action) => {
  switch (action.type) {
    case types.TO_DIALOG_CREATE:
      return {
        ...state,
        status: status.DIALOG_CREATE,
        opponent_id: action.opponent_id
      };
    case types.TO_DIALOG_VIEW:
      return {
        ...state,
        status: status.DIALOG_VIEW,
        dialog_id: action.dialog_id
      };
    case types.TO_DIALOG_LIST:
      return {
        ...state,
        status: status.DIALOG_LIST
      };
    case types.SAVE_DIALOG_LIST:
      return {
        ...state,
        dialogs: action.dialogs
      };
    default:
      return state;
  }
};
