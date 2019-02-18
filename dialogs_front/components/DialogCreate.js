import React from "react";
import * as actions from "../actions/viewActions";
import { connect } from "react-redux";

class DialogCreate extends React.Component {
  state = {
    dialogs: []
  };

  handleSubmit = event => {
    event.preventDefault();
    this.props.toDialogView(35);
  };

  render() {
    return (
      <div>
        <h4>Отправить сообщение</h4>
        <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            <label htmlFor="themeInputId">Тема сообщения</label>
            <input type="text" className="form-control" id="themeInputId" />
          </div>
          <div className="form-group">
            <label htmlFor="textMessageInputId">Текст сообщения:</label>
            <textarea
              className="form-control"
              id="textMessageInputId"
              rows="8"
              name="text"
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Отправить
          </button>
        </form>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  opponent_id: state.opponent_id
});

export default connect(
  mapStateToProps,
  actions
)(DialogCreate);
