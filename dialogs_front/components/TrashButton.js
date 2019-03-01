import React from "react";
import AnimateThis from "./AnimateThis";

class TrashButton extends React.Component {
  state = {
    showConfirm: false
  };

  handleClick = event => {
    event.stopPropagation();
    this.setState(state => ({ showConfirm: !state.showConfirm }));
  };

  handleDelete = event => {
    event.stopPropagation();
    this.props.onDelete();
  };

  render() {
    return (
      <AnimateThis>
        {this.state.showConfirm ? (
          <div key={0}>
            Вы уверены?
            <button
              className="btn btn-outline-danger btn-sm mr-1 ml-2"
              onClick={this.handleDelete}
            >
              Да
            </button>
            <button
              className="btn btn-outline-success btn-sm"
              onClick={this.handleClick}
            >
              Нет
            </button>
          </div>
        ) : (
          <div key={1}>
            <button
              className="btn btn-outline-danger btn-sm"
              onClick={this.handleClick}
            >
              <i className="fa fa-trash-o" aria-hidden="true" />
            </button>
          </div>
        )}
      </AnimateThis>
    );
  }
}

export default TrashButton;
