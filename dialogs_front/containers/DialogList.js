import { connect } from "react-redux";
import * as actions from "../actions/viewActions";
import DialogList from "../components/DialogList";

export default connect(
  () => ({}),
  actions
)(DialogList);
