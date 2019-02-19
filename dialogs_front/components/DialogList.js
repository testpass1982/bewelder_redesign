import React from "react";
import DialogListItem from "./DialogListItem";

class DialogList extends React.Component {
  state = {
    dialogs: [
      {
        id: 1,
        theme: "Предложение от ГазПрома"
      },
      {
        id: 2,
        theme: "Не хотите поработать на Новой Земле?"
      }
    ]
  };

  render() {
    const dialogs = this.state.dialogs.map(dialog => (
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
        <div className="list-group">{dialogs}</div>
      </div>
    );
  }
}

export default DialogList;
