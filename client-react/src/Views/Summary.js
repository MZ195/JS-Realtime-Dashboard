import React, { Component } from "react";
import up from "../img/money-up.svg";
import down from "../img/money-down.svg";
import savings from "../img/saving.svg";

class Summary extends Component {
  constructor() {
    super();
    this.state = {
      data: {},
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://localhost:9000/pos_count/")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ data: data });
        });
    }, 30000);
  }

  render() {
    const { data } = this.state;

    return (
      <div className="col-12">
        <div className="card">
          <div className="card-content">
            <div className="card-body">
              <div className="row">
                <div className="col-xl-4 col-lg-6 col-md-12 border-right border-grey border-right border-lighten-3 clearfix">
                  <div className="float-left pl-2 block-content">
                    <span className="grey darken-1 block title">
                      Positive Tweets
                    </span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      {Number(data["Total_pos"]).toLocaleString()}
                      <img src={up} alt="" />
                    </div>
                  </div>
                </div>
                <div className="col-xl-4 col-lg-6 col-md-12 border-right border-grey border-right border-lighten-3 clearfix">
                  <div className="float-left pl-2 block-content">
                    <span className="title">Negative Tweets</span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      {Number(data["Total_neg"]).toLocaleString()}
                      <img src={down} alt="" />
                    </div>
                  </div>
                </div>
                <div className="col-xl-4 col-lg-6 col-md-12 clearfix">
                  <div className="float-left pl-2 block-content">
                    <span className="title">Model Score</span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      {Number(data["savings_avg"]).toLocaleString()}
                      <img src={savings} alt="" />
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