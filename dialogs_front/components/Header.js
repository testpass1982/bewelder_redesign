import React from "react";
import * as statusView from "../constants/status";

const Header = ({ status, dialog }) => {
  let title = <h2>Ваши сообщения</h2>;
  console.log(dialog.members);
  console.log(status);
  if (status === statusView.DIALOG_VIEW) {
    if (dialog.members) {
      const creator = dialog.members.filter(member => member.is_creator)[0];
      title = (
        <h2>
          {creator.name}: {dialog.theme}
        </h2>
      );
    }
  } else if (status === statusView.DIALOG_CREATE) {
    title = <h2>Оставить сообщение</h2>;
  }
  return title;
};

export default Header;
