import * as types from "../constants/actionTypes";
import * as status from "../constants/status";

export default (state = {}, action) => {
  switch (action.type) {
    case types.TO_DIALOG_CREATE:
      return {
        ...state,
        status: status.DIALOG_CREATE,
        opponentId: action.opponentId
      };
    case types.TO_DIALOG_VIEW:
      return {
        ...state,
        status: status.DIALOG_VIEW,
        dialog: { id: action.dialogId }
      };
    case types.TO_DIALOG_LIST:
      return {
        ...state,
        status: status.DIALOG_LIST
      };
    case types.SAVE_DIALOG_LIST:
      return {
        ...state,
        dialogSet: action.dialogSet
      };
    case types.SAVE_DIALOG:
      return {
        ...state,
        dialog: action.dialog
      };
    case types.APPEND_MESSAGE:
      if (state.status === status.DIALOG_VIEW) {
        const dialog = {
          ...state.dialog
        };
        if (dialog.message_set) {
          dialog.message_set = [...state.dialog.message_set, action.message];
        } else {
          dialog.message_set = [action.message];
        }
        return {
          ...state,
          dialog
        };
      }
    case types.DELETE_DIALOG:
      if (!state.dialogSet) return { ...state };
      let dialogSet = [...state.dialogSet].filter(
        dialog => dialog.id != action.dialogId
      );
      return { ...state, dialogSet };
    default:
      return state;
  }
};
