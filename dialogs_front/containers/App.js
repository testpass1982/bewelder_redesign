import { connect } from "react-redux";
import App from "../components/App";

const mapStateToProps = state => ({
  status: state.status,
  loading: state.loading
});

export default connect(mapStateToProps)(App);
