import React from "react";
import Header from "./Header";
import DialogList from "./DialogList";

class App extends React.Component {
  state = {};

  render() {
    return (
      <div className="container">
        <Header />
        <DialogList />
      </div>
    );
  }
}

export default App;
