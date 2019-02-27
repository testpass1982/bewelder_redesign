import { connect } from "react-redux";
import Header from "../components/Header";

const mapStateToProps = state => ({
  status: state.status,
  dialog: state.dialog
});

export default connect(mapStateToProps)(Header);
