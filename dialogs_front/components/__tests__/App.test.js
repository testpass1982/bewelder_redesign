import React from "react";
import { createRenderer } from "react-test-renderer/shallow";
import * as status from "../../constants/status";
import App from "../App";
import Header from "../../containers/Header";
import DialogList from "../../containers/DialogList";
import DialogCreate from "../../containers/DialogCreate";
import DialogView from "../../containers/DialogView";

const setup = propOverides => {
  const props = Object.assign(
    {
      status: undefined
    },
    propOverides
  );

  const renderer = createRenderer();
  renderer.render(<App {...props} />);
  const output = renderer.getRenderOutput();

  return {
    output,
    renderer
  };
};

test("Header should render", () => {
  const { output } = setup();
  const [header] = output.props.children;
  expect(header.type).toBe(Header);
});

test("DialogList should render by default", () => {
  const { output } = setup();
  const [, dialogList] = output.props.children;
  expect(dialogList.type).toBe(DialogList);
});

test("DialogCreate should render with status DIALOG_CREATE", () => {
  const { output } = setup({ status: status.DIALOG_CREATE });
  const [, dialogCreate] = output.props.children;
  expect(dialogCreate.type).toBe(DialogCreate);
});

test("DialogList should render with status DIALOG_LIST", () => {
  const { output } = setup({ status: status.DIALOG_LIST });
  const [, dialogList] = output.props.children;
  expect(dialogList.type).toBe(DialogList);
});

test("DialogView should render with status DIALOG_VIEW", () => {
  const { output } = setup({ status: status.DIALOG_VIEW });
  const [, dialogView] = output.props.children;
  expect(dialogView.type).toBe(DialogView);
});
