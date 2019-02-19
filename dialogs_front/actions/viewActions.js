import * as types from "../constants/actionTypes";

export function toDialogList() {
  return {
    type: types.TO_DIALOG_LIST
  };
}

export function toDialogView(dialog_id) {
  return {
    type: types.TO_DIALOG_VIEW,
    dialog_id
  };
}

export function toDialogCreate(opponent_id) {
  return {
    type: types.TO_DIALOG_CREATE,
    opponent_id
    // TODO: vacancy_id
  };
}
