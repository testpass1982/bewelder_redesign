import { connect } from "react-redux";
import App from "../components/App";

const mapStateToProps = state => ({
  status: state.status
});

export default connect(mapStateToProps)(App);
