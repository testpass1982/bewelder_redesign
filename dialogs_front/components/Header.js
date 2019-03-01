import React from "react";
import * as statusView from "../constants/status";
import AnimateThis from "./AnimateThis";

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
    <AnimateThis>
      <div key={key}>
        <h3>{title}</h3>
      </div>
    </AnimateThis>
  );
};

export default Header;
