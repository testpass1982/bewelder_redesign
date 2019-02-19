import { connect } from "react-redux";
import * as actions from "../actions/viewActions";
import DialogCreate from "../components/DialogCreate";

const mapStateToProps = state => ({
  opponent_id: state.opponent_id
});

export default connect(
  mapStateToProps,
  actions
)(DialogCreate);
