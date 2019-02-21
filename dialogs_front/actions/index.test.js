import * as types from "../constants/actionTypes";
import * as actions from "./index";

test("toDialogList should create TO_DIALOG_LIST action", () => {
  expect(actions.toDialogList()).toEqual({
    type: types.TO_DIALOG_LIST
  });
});

test("toDialogView should create TO_DIALOG_VIEW action", () => {
  expect(actions.toDialogView(42)).toEqual({
    type: types.TO_DIALOG_VIEW,
    dialogId: 42
  });
});

test("toDialogCreate should create TO_DIALOG_CREATE action", () => {
  expect(actions.toDialogCreate(23)).toEqual({
    type: types.TO_DIALOG_CREATE,
    opponentId: 23
  });
});

test("saveDialogList should create SAVE_DIALOG_LIST action", () => {
  expect(actions.saveDialogList([{ id: 1 }, { id: 2 }])).toEqual({
    type: types.SAVE_DIALOG_LIST,
    dialogs: [{ id: 1 }, { id: 2 }]
  });
});

test("saveDialog should create SAVE_DIALOG action", () => {
  expect(actions.saveDialog({ id: 1, messages: [] })).toEqual({
    type: types.SAVE_DIALOG,
    dialog: { id: 1, messages: [] }
  });
});

test("appendMessage should create APPEND_MESSAGE action", () => {
  expect(actions.appendMessage({ id: 1, text: "foo bar" })).toEqual({
    type: types.APPEND_MESSAGE,
    message: { id: 1, text: "foo bar" }
  });
});
