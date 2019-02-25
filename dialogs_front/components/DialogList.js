import React from "react";
import DialogListItem from "./DialogListItem";
import api from "../utils/api";

class DialogList extends React.Component {
  componentDidMount() {
    api.dialogs.get().then(dialogSet => {
      if (JSON.stringify(dialogSet) !== JSON.stringify(this.props.dialogSet)) {
        this.props.saveDialogList(dialogSet);
      }
    });
  }

  render() {
    const dialogs = this.props.dialogSet.map(dialog => (
      <a
        href="#"
        className="list-group-item list-group-item-action"
        key={dialog.id}
        onClick={() => {
          this.props.toDialogView(dialog.id);
        }}
      >
        <DialogListItem dialog={dialog} />
      </a>
    ));
    return (
      <div className="my-3">
        {dialogs.length ? (
          <div className="list-group">{dialogs}</div>
        ) : (
          <div>У Вас пока нет сообщений</div>
        )}
      </div>
    );
  }
}

export default DialogList;
