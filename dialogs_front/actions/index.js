import * as types from "../constants/actionTypes";

export const toDialogList = () => ({
  type: types.TO_DIALOG_LIST
});

export const toDialogView = dialog_id => ({
  type: types.TO_DIALOG_VIEW,
  dialog_id
});

export const toDialogCreate = opponent_id => ({
  type: types.TO_DIALOG_CREATE,
  opponent_id
  // TODO: vacancy_id
});

export const saveDialogList = dialogs => ({
  type: types.SAVE_DIALOG_LIST,
  dialogs
});
