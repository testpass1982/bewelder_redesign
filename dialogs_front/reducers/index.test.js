import * as types from "../constants/actionTypes";
import * as status from "../constants/status";
import reducer from "./index";

test("reducer should handle TO_DIALOG_CREATE", () => {
  expect(
    reducer(
      {},
      {
        type: types.TO_DIALOG_CREATE,
        opponentId: 42
      }
    )
  ).toEqual({
    status: status.DIALOG_CREATE,
    opponentId: 42
  });

  expect(
    reducer(
      {
        status: status.DIALOG_VIEW,
        dialogId: 23
      },
      {
        type: types.TO_DIALOG_CREATE,
        opponentId: 42
      }
    )
  ).toMatchObject({
    status: status.DIALOG_CREATE,
    opponentId: 42
  });
});

test("reducer should handle TO_DIALOG_VIEW", () => {
  expect(
    reducer(
      {},
      {
        type: types.TO_DIALOG_VIEW,
        dialogId: 42
      }
    )
  ).toEqual({
    status: status.DIALOG_VIEW,
    dialog: { id: 42 }
  });

  expect(
    reducer(
      {
        status: status.DIALOG_CREATE,
        opponentId: 23
      },
      {
        type: types.TO_DIALOG_VIEW,
        dialogId: 42
      }
    )
  ).toMatchObject({
    status: status.DIALOG_VIEW,
    dialog: { id: 42 }
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
        dialog: { id: 23 }
      },
      {
        type: types.TO_DIALOG_LIST
      }
    )
  ).toMatchObject({
    status: status.DIALOG_LIST
  });
});

test("reducer should handle SAVE_DIALOG_LIST", () => {
  expect(
    reducer(
      {},
      {
        type: types.SAVE_DIALOG_LIST,
        dialogs: [{ id: 1 }, { id: 2 }]
      }
    )
  ).toMatchObject({
    dialogs: [{ id: 1 }, { id: 2 }]
  });

  expect(
    reducer(
      {
        status: status.DIALOG_VIEW,
        dialog: { id: 23 }
      },
      {
        type: types.SAVE_DIALOG_LIST,
        dialogs: [{ id: 1 }, { id: 2 }]
      }
    )
  ).toMatchObject({
    status: status.DIALOG_VIEW,
    dialog: { id: 23 },
    dialogs: [{ id: 1 }, { id: 2 }]
  });
});

test("reducer should handle SAVE_DIALOG", () => {
  expect(
    reducer(
      {},
      {
        type: types.SAVE_DIALOG,
        dialog: { id: 1, messages: [] }
      }
    )
  ).toMatchObject({
    dialog: { id: 1, messages: [] }
  });

  expect(
    reducer(
      {
        status: status.DIALOG_VIEW,
        dialog: { id: 23 }
      },
      {
        type: types.SAVE_DIALOG,
        dialog: { id: 1, messages: [] }
      }
    )
  ).toMatchObject({
    status: status.DIALOG_VIEW,
    dialog: { id: 23 },
    dialog: { id: 1, messages: [] }
  });
});

describe("reducer should handle APPEND_MESSAGE", () => {
  test("do not append a new message if status is not DIALOG_VIEW", () => {
    expect(
      reducer(
        { status: status.DIALOG_LIST },
        {
          type: types.APPEND_MESSAGE,
          message: { id: 23, text: "foo bar" }
        }
      )
    ).toEqual({ status: status.DIALOG_LIST });
  });

  test("append a new message to dialog message_set", () => {
    expect(
      reducer(
        {
          status: status.DIALOG_VIEW,
          dialog: {
            id: 42
          }
        },
        {
          type: types.APPEND_MESSAGE,
          message: { id: 23, text: "foo bar" }
        }
      )
    ).toEqual({
      status: status.DIALOG_VIEW,
      dialog: {
        id: 42,
        message_set: [{ id: 23, text: "foo bar" }]
      }
    });

    expect(
      reducer(
        {
          status: status.DIALOG_VIEW,
          dialog: {
            id: 42,
            message_set: []
          }
        },
        {
          type: types.APPEND_MESSAGE,
          message: { id: 23, text: "foo bar" }
        }
      )
    ).toEqual({
      status: status.DIALOG_VIEW,
      dialog: {
        id: 42,
        message_set: [{ id: 23, text: "foo bar" }]
      }
    });

    expect(
      reducer(
        {
          status: status.DIALOG_VIEW,
          dialog: {
            id: 42,
            message_set: [{ id: 23, text: "foo bar" }]
          }
        },
        {
          type: types.APPEND_MESSAGE,
          message: { id: 24, text: "bar foo" }
        }
      )
    ).toEqual({
      status: status.DIALOG_VIEW,
      dialog: {
        id: 42,
        message_set: [{ id: 23, text: "foo bar" }, { id: 24, text: "bar foo" }]
      }
    });
  });
});
