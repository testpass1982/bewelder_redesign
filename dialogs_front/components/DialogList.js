import React from "react";
import { CSSTransitionGroup } from "react-transition-group";
import DialogData from "./DialogData";
import api from "../utils/api";
import "./animation.css";
import TrashButton from "./TrashButton";

class DialogList extends React.Component {
  componentDidMount() {
    api.dialogs.get().then(dialogSet => {
      if (JSON.stringify(dialogSet) !== JSON.stringify(this.props.dialogSet)) {
        this.props.saveDialogList(dialogSet);
      }
    });
  }

  handleDelete = id => {
    api.dialogs.delete(id).then(() => this.props.deleteDialog(id));
  };

  render() {
    const dialogs = this.props.dialogSet.map(dialog => (
      <a
        href="#"
        className="list-group-item list-group-item-action "
        key={dialog.id}
        onClick={() => {
          this.props.toDialogView(dialog.id);
        }}
      >
        <div className="d-flex justify-content-between">
          <DialogData dialog={dialog} />
          <TrashButton onDelete={() => this.handleDelete(dialog.id)} />
        </div>
      </a>
    ));
    return (
      <div className="my-3">
        {dialogs.length ? (
          <div
            className="list-group"
            style={{ height: "70vh", overflow: "auto" }}
          >
            <CSSTransitionGroup
              transitionName="slide"
              transitionAppear={true}
              transitionAppearTimeout={1000}
              transitionEnterTimeout={1000}
              transitionLeaveTimeout={1000}
            >
              {dialogs}
            </CSSTransitionGroup>
          </div>
        ) : (
          <div>У Вас пока нет сообщений</div>
        )}
      </div>
    );
  }
}

export default DialogList;
