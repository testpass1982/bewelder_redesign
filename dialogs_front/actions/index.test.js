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
    dialog_id: 42
  });
});

test("toDialogCreate should create TO_DIALOG_CREATE action", () => {
  expect(actions.toDialogCreate(23)).toEqual({
    type: types.TO_DIALOG_CREATE,
    opponent_id: 23
  });
});

test("saveDialogList should create SAVE_DIALOG_LIST action", () => {
  expect(actions.saveDialogList([{ id: 1 }, { id: 2 }])).toEqual({
    type: types.SAVE_DIALOG_LIST,
    dialogs: [{ id: 1 }, { id: 2 }]
  });
});
