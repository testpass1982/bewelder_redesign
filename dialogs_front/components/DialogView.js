import React from "react";
import * as actions from "../actions/viewActions";
import { connect } from "react-redux";
import MessageList from "./MessageList";

class DialogView extends React.Component {
  state = {
    messages: [
      {
        id: 1,
        user: "Adam",
        text:
          "Добрый день! Нам требуется работник для работы на работе. Предлагаем зарплату деньгами. Что Вы об этом думаете?"
      },
      {
        id: 2,
        user: "Eva",
        text: "Отлично!!! Куда прийти? Вещи брать?"
      }
    ]
  };

  handleSubmit = event => {
    event.preventDefault();
    console.log("send message");
  };

  render() {
    return (
      <div>
        <button
          onClick={this.props.toDialogList}
          className="btn btn-secondary my-3"
        >
          К списку сообщений
        </button>
        {/* <h4>Dialog view</h4>
        <h5>{this.props.dialog_id}</h5> */}
        <MessageList messages={this.state.messages} />
        <div>
          <form onSubmit={this.handleSubmit}>
            <div className="input-group">
              <textarea className="form-control" rows="8" />
              <div className="input-group-append">
                <button className="btn btn-success" type="submit">
                  Отправить
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  dialog_id: state.dialog_id
});

export default connect(
  mapStateToProps,
  actions
)(DialogView);
