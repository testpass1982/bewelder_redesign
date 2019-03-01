import React from "react";
import DialogData from "./DialogData";
import api from "../utils/api";
import TrashButton from "./TrashButton";
import AnimateThis from "./AnimateThis";

class DialogList extends React.Component {
  state = {
    filterValue: ""
  };

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

  handleFilterChange = event => {
    this.setState({ filterValue: event.target.value });
  };

  render() {
    const dialogs = this.props.dialogSet
      .filter(dialog => {
        const creator = dialog.members.find(e => e.is_creator);
        const s = `${creator.name} ${dialog.theme}`.toLowerCase();
        return s.indexOf(this.state.filterValue.toLowerCase()) > -1;
      })
      .map(dialog => (
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
        <div className="form-group has-feedback">
          <input
            type="text"
            className="form-control"
            placeholder="Искать переписку"
            value={this.state.filterValue}
            onChange={this.handleFilterChange}
          />
          <i
            className="fa fa-search text-success"
            style={{ float: "right", margin: "-28px 10px" }}
          />
        </div>
        {dialogs.length ? (
          <div
            className="list-group"
            style={{ height: "70vh", overflow: "auto" }}
          >
            <AnimateThis transitionLeave>{dialogs}</AnimateThis>
          </div>
        ) : (
          <div>У Вас пока нет сообщений</div>
        )}
      </div>
    );
  }
}

export default DialogList;
