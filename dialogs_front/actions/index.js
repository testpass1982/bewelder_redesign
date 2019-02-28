import * as types from "../constants/actionTypes";

export const toDialogList = () => ({
  type: types.TO_DIALOG_LIST
});

export const toDialogView = dialogId => {
  return {
    type: types.TO_DIALOG_VIEW,
    dialogId
  };
};

export const toDialogCreate = opponentId => ({
  type: types.TO_DIALOG_CREATE,
  opponentId
  // TODO: vacancy_id
});

export const saveDialogList = dialogSet => ({
  type: types.SAVE_DIALOG_LIST,
  dialogSet
});

export const saveDialog = dialog => ({
  type: types.SAVE_DIALOG,
  dialog
});

export const appendMessage = message => ({
  type: types.APPEND_MESSAGE,
  message
});
