import React from "react";
import * as statusView from "../constants/status";
import { CSSTransitionGroup } from "react-transition-group";
import "./animation.css";

const Header = ({ status, dialog }) => {
  let title = "Ваши сообщения";
  let key = 0;
  if (status === statusView.DIALOG_VIEW) {
    if (dialog.members) {
      const creator = dialog.members.filter(member => member.is_creator)[0];
      title = `${creator.name}: ${dialog.theme}`;
      key = 1;
    }
  } else if (status === statusView.DIALOG_CREATE) {
    title = "Оставить сообщение";
  }
  return (
    <CSSTransitionGroup
      transitionName="slide"
      transitionAppear={true}
      transitionAppearTimeout={1000}
      transitionEnterTimeout={1000}
      transitionLeave={false}
    >
      <div key={key}>
        <h3>{title}</h3>
      </div>
    </CSSTransitionGroup>
  );
};

export default Header;
