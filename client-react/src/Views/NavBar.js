import React, { Component } from "react";
import chartIcon from "../img/chart-icon.svg";

class NavBar extends Component {
  render() {
    return (
      <div id="navbar" className="sticky">
        <div className="col-lg-4 d-flex navBarIcon">
          <img src={chartIcon} alt="" />
          <h2>Bitcon Real-Time Predictive Analysis</h2>
        </div>
      </div>
    );
  }
}

export default NavBar;
