import * as types from "../constants/actionTypes";
import * as status from "../constants/status";
import reducer from "./index";

test("reducer should handle TO_DIALOG_CREATE", () => {
  expect(
    reducer(
      {},
      {
        type: types.TO_DIALOG_CREATE,
        opponent_id: 42
      }
    )
  ).toEqual({
    status: status.DIALOG_CREATE,
    opponent_id: 42
  });

  expect(
    reducer(
      {
        status: status.DIALOG_VIEW,
        dialog_id: 23
      },
      {
        type: types.TO_DIALOG_CREATE,
        opponent_id: 42
      }
    )
  ).toEqual({
    status: status.DIALOG_CREATE,
    opponent_id: 42
  });
});

test("reducer should handle TO_DIALOG_VIEW", () => {
  expect(
    reducer(
      {},
      {
        type: types.TO_DIALOG_VIEW,
        dialog_id: 42
      }
    )
  ).toEqual({
    status: status.DIALOG_VIEW,
    dialog_id: 42
  });

  expect(
    reducer(
      {
        status: status.DIALOG_CREATE,
        opponent_id: 23
      },
      {
        type: types.TO_DIALOG_VIEW,
        dialog_id: 42
      }
    )
  ).toEqual({
    status: status.DIALOG_VIEW,
    dialog_id: 42
  });
});

test("reducer should handle TO_DIALOG_LIST", () => {
  expect(
    reducer(
      {},
      {
        type: types.TO_DIALOG_LIST
      }
    )
  ).toEqual({
    status: status.DIALOG_LIST
  });

  expect(
    reducer(
      {
        status: status.DIALOG_VIEW,
        dialog_id: 23
      },
      {
        type: types.TO_DIALOG_LIST
      }
    )
  ).toEqual({
    status: status.DIALOG_LIST
  });
});
