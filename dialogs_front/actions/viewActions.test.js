import * as types from "../constants/actionTypes";
import * as actions from "./viewActions";

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

test("toDialogCreate should create TO_DIALOG_CREATE  actions", () => {
  expect(actions.toDialogCreate(23)).toEqual({
    type: types.TO_DIALOG_CREATE,
    opponent_id: 23
  });
});
