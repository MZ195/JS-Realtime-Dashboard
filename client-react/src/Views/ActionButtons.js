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

    var statement = "";
    var sell_buy_action = null;
    var style = "";

    if (BTC_last_operation["operation"] === "SELL") {
      sell_buy_action = (e) =>
        fetch("http://localhost:9000/btc/recommendation/buy");
      statement = "BUY";
      style = "card-body-action-buy";
    } else {
      sell_buy_action = (e) =>
        fetch("http://localhost:9000/btc/recommendation/sell");
      statement = "SELL";
      style = "card-body-action-sell";
    }

    return (
      <div className="col">
        <div className="card border-0 action-buttons">
          <div className="card-content-action">
            <div className={style}>
              <div className="row">
                <div className="col ">
                  <div
                    onClick={sell_buy_action}
                    className="font-large-3 line-height-1 text-bold-33 value value-action-sell"
                  >
                    {statement}
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
