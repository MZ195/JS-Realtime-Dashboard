import React, { Component } from "react";
import up from "../img/money-up.svg";
import down from "../img/money-down.svg";
import savings from "../img/saving.svg";

class Summary extends Component {
  constructor() {
    super();
    this.state = {
      data: {},
      model_score: {},
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://127.0.0.1:9000/tweets/count")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ data: data });
        });

      fetch("http://127.0.0.1:9000/score/overall")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ model_score: data });
        });
    }, 15000);
  }

  render() {
    const { data } = this.state;
    const { model_score } = this.state;

    return (
      <div className="col-12">
        <div className="card border-0">
          <div className="card-content">
            <div className="card-body">
              <div className="row">
                <div className="col-xl-4 col-lg-6 col-md-12 border-right clearfix">
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
                <div className="col-xl-4 col-lg-6 col-md-12 border-right clearfix">
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
                    <span className="title">Model Score (R Squared)</span>
                    <div className="font-large-3 line-height-1 text-bold-33 value">
                      <p>
                        <img src={savings} alt="" />
                        {(Number(model_score["R2"]) * 100).toLocaleString()} %
                      </p>
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
