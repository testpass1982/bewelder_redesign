import React from "react";
import DialogData from "./DialogData";
import api from "../utils/api";
import TrashButton from "./TrashButton";
import AnimateThis from "./AnimateThis";
import FilterForm from "./FilterForm";

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

  getDialogs = () => {
    const dialogs = this.props.dialogSet
      .filter(dialog => {
        const creatorIndex = dialog.members.findIndex(e => e.is_creator);
        const creator = dialog.members[creatorIndex];
        const opponent = dialog.members[1 - creatorIndex];
        const s = `${creator.name} ${opponent ? opponent.name : ""} ${
          dialog.theme
        }`.toLowerCase();
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
    return dialogs;
  };

  render() {
    const dialogs = this.getDialogs();

    return (
      <div className="my-3">
        <FilterForm
          value={this.state.filterValue}
          onFilterChange={this.handleFilterChange}
        />
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
