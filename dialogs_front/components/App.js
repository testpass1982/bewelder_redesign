import React from "react";
import Header from "./Header";
import DialogList from "./DialogList";
import { DIALOG_CREATE, DIALOG_LIST, DIALOG_VIEW } from "../constants/status";
import DialogCreate from "./DialogCreate";
import DialogView from "./DialogView";
import { connect } from "react-redux";

class App extends React.Component {
  state = {
    dialogs: []
  };

  render() {
    console.log("render App");
    const status = this.props.status;
    console.log("status:", status);
    let view;
    switch (status) {
      case DIALOG_CREATE:
        view = <DialogCreate />;
        break;
      case DIALOG_LIST:
        view = <DialogList />;
        break;
      case DIALOG_VIEW:
        view = <DialogView />;
        break;
      default:
        view = <DialogList />;
    }
    return (
      <div className="m-5">
        <Header />
        {view}
      </div>
    );
  }
}

const mapStateToProps = state => ({
  status: state.status
});

export default connect(mapStateToProps)(App);
