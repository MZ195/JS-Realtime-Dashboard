import React, { Component } from "react";
import wallet from "../img/money-bag.svg";
import exchange_green from "../img/exchange.svg";
import exchange_red from "../img/exchange-red.svg";
import discount from "../img/discount.svg";
import auction from "../img/auction.svg";
import accuracy from "../img/accuracy.svg";
import returns from "../img/return.svg";

class Summary extends Component {
  constructor() {
    super();
    this.state = {
      model_score: {},
      profit: {},
      deals: {},
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://127.0.0.1:9000/btc/profit")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ profit: data });
        });

      fetch("http://127.0.0.1:9000/score/overall")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ model_score: data });
        });

      fetch("http://localhost:9000/btc/profit/deals")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ deals: data });
        });
    }, 15000);
  }

  render() {
    const { profit } = this.state;
    const { model_score } = this.state;
    const { deals } = this.state;

    return (
      <div className="col">
        <div className="card border-0">
          <div className="card-content">
            <div className="card-body">
              <div className="row">
                <div className="col-xl-2 col-lg-6 col-md-12 border-right clearfix">
                  <div className="float-left pl-2 block-content">
                    <span className="grey darken-1 block title">
                      Initial Investment
                    </span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      10,000 $
                      <img src={wallet} alt="" />
                    </div>
                  </div>
                </div>
                <div className="col-xl-2 col-lg-6 col-md-12 border-right clearfix">
                  <div className="float-left pl-2 block-content">
                    <span className="title">Return Percentage</span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      {Number(profit["rtn_pct"]) !== 0
                        ? (Number(profit["rtn_pct"]) - 100)
                            .toFixed(2)
                            .toLocaleString()
                        : Number(profit["rtn_pct"])
                            .toFixed(2)
                            .toLocaleString()}{" "}
                      %
                      <img src={discount} alt="" />
                    </div>
                  </div>
                </div>
                <div className="col-xl-2 col-lg-6 col-md-12 border-right clearfix">
                  <div className="float-left pl-2 block-content">
                    <span className="title">Profit/Loss</span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      {Number(profit["profit_loss"]).toLocaleString()} $
                      <img
                        src={
                          Number(profit["profit_loss"]) > 0
                            ? exchange_green
                            : exchange_red
                        }
                        alt=""
                      />
                    </div>
                  </div>
                </div>
                <div className="col-xl-2 col-lg-6 col-md-12 border-right clearfix">
                  <div className="float-left pl-2 block-content">
                    <span className="title">Runing Amount</span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      {Number(profit["runing_amount"]).toLocaleString()} $
                      <img src={returns} alt="" />
                    </div>
                  </div>
                </div>
                <div className="col-xl-2 col-lg-6 col-md-12 border-right clearfix">
                  <div className="float-left pl-2 block-content">
                    <span className="title">Number of Deals</span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      {Number(deals["count"]).toLocaleString()}
                      <img src={auction} alt="" />
                    </div>
                  </div>
                </div>
                <div className="col-xl-2 col-lg-6 col-md-12 clearfix">
                  <div className="float-left pl-2 block-content">
                    <span className="title">Model Score (R²)</span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      {(Number(model_score["R2"]) * 100)
                        .toFixed(2)
                        .toLocaleString()}{" "}
                      %
                      <img src={accuracy} alt="" />
                    </div>
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

export default Summary;
