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
  const [, cssTransitionGroup] = output.props.children;
  const div = cssTransitionGroup.props.children;
  const view = div.props.children;
  expect(view.type).toBe(DialogList);
});

test("DialogCreate should render with status DIALOG_CREATE", () => {
  const { output } = setup({ status: status.DIALOG_CREATE });
  const [, cssTransitionGroup] = output.props.children;
  const div = cssTransitionGroup.props.children;
  const view = div.props.children;
  expect(view.type).toBe(DialogCreate);
});

test("DialogList should render with status DIALOG_LIST", () => {
  const { output } = setup({ status: status.DIALOG_LIST });
  const [, cssTransitionGroup] = output.props.children;
  const div = cssTransitionGroup.props.children;
  const view = div.props.children;
  expect(view.type).toBe(DialogList);
});

test("DialogView should render with status DIALOG_VIEW", () => {
  const { output } = setup({ status: status.DIALOG_VIEW });
  const [, cssTransitionGroup] = output.props.children;
  const div = cssTransitionGroup.props.children;
  const view = div.props.children;
  expect(view.type).toBe(DialogView);
});
