import React from "react";
import Header from "./Header";
import { DIALOG_CREATE, DIALOG_LIST, DIALOG_VIEW } from "../constants/status";
import DialogList from "../containers/DialogList";
import DialogCreate from "../containers/DialogCreate";
import DialogView from "../containers/DialogView";

class App extends React.Component {
  state = {
    dialogs: []
  };

  componentWillUnmount() {
    console.log("dialogs app will unmount");
  }

  render() {
    const status = this.props.status;
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

export default App;
