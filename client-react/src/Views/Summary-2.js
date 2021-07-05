import React, { Component } from "react";
import auction from "../img/auction.svg";
import accuracy from "../img/accuracy.svg";
import returns from "../img/return.svg";

class Summary2 extends Component {
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
    const { model_score } = this.state;
    const { profit } = this.state;
    const { deals } = this.state;

    return (
      <div className="col">
        <div className="card border-0">
          <div className="card-content">
            <div className="card-body">
              <div className="row">
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

export default Summary2;
