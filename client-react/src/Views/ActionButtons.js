import React, { Component } from "react";

class ActionButtons extends Component {
  constructor() {
    super();
    this.state = {
      BTC_last_operation: {},
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://localhost:9000/btc/profit/details/lastOperation")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ BTC_last_operation: data });
        });
    }, 15000);
  }

  render() {
    const { BTC_last_operation } = this.state;

    return (
      <div className="col">
        <div className="card border-0 action-buttons">
          <div className="card-content">
            <div className="card-body">
              <div className="row">
                <div className="col ">
                  <span className="title">Last Operation</span>
                  <div className="font-large-3 line-height-1 text-bold-33 value">
                    Time: {BTC_last_operation["datetime"]} | Operation:{" "}
                    {BTC_last_operation["operation"]} | Price:{" "}
                    {Number(BTC_last_operation["price"]).toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default ActionButtons;
