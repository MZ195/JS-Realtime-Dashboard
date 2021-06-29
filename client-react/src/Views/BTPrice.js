import React, { Component } from "react";
import { Line } from "react-chartjs-2";
import { BigNumber } from "bignumber.js";

class BTPrice extends Component {
  constructor() {
    super();
    this.state = {
      BTC_Data: [],
      BTC_Prediction_ARIMA: [],
      BTC_Prediction_VARMAX: [],
      BTC_Prediction_SES: [],
      BTC_Prediction_overall: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      var v = new Date();
      if (
        v.getSeconds() === 33 ||
        v.getSeconds() === 3 ||
        v.getSeconds() === 13 ||
        v.getSeconds() === 43
      ) {
        fetch("http://localhost:9000/btc/price")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Data: data });
          });

        fetch("http://localhost:9000/predict/ARIMA")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Prediction_ARIMA: data });
          });

        fetch("http://localhost:9000/predict/VARMAX")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Prediction_VARMAX: data });
          });

        fetch("http://localhost:9000/predict/SES")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Prediction_SES: data });
          });

        fetch("http://localhost:9000/predict/overall")
          .then((res) => res.json())
          .then((data) => {
            this.setState({ BTC_Prediction_overall: data });
          });
      }
    }, 60);
  }

  render() {
    const { BTC_Data } = this.state;
    const { BTC_Prediction_ARIMA } = this.state;
    const { BTC_Prediction_VARMAX } = this.state;
    const { BTC_Prediction_SES } = this.state;
    const { BTC_Prediction_overall } = this.state;

    let chartJSData = {
      labels: [],
      datasets: [
        {
          label: "BTC Price",
          data: [],
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(31, 217, 154, 0.9)",
          // fill: true,
          backgroundColor: "rgba(31, 217, 154, 0.03)",
        },
        {
          label: "BTC Price ARIMA",
          data: [],
          hidden: true,
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(139, 68, 246, 0.9)",
          // fill: true,
          backgroundColor: "rgba(139, 68, 246, 0.03)",
        },
        {
          label: "BTC Price VARMAX",
          data: [],
          hidden: true,
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(255, 166, 0, 0.9)",
          // fill: true,
          backgroundColor: "rgba(255, 166, 0, 0.03)",
        },
        {
          label: "BTC Price SES",
          data: [],
          hidden: true,
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(33, 150, 243, 0.9)",
          // fill: true,
          backgroundColor: "rgba(33, 150, 243, 0.03)",
        },
        {
          label: "BTC Price Overall",
          data: [],
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(255, 98, 88, 0.9)",
          // fill: true,
          backgroundColor: "rgba(255, 98, 88, 0.03)",
        },
      ],
    };

    BTC_Data.forEach((item) => {
      chartJSData.labels.push(item.datetime);
      chartJSData.datasets[0].data.push(item.price);
      chartJSData.datasets[0].pointBackgroundColor.push(
        "rgba(31, 217, 154, 0.9)"
      );
    });

    BTC_Prediction_ARIMA.forEach((item) => {
      if (!chartJSData.labels.includes(item.datetime)) {
        var currentHour = item.datetime.substring(0, 2);
        var currentMinutes = item.datetime.substring(3, 5);
        var currentSeconds = item.datetime.substring(6, 8);
        var dateLimit = new Date(new Date() - 28 * 60000);
        var v = new Date();
        v.setMinutes(currentMinutes);
        v.setSeconds(currentSeconds);
        v.setHours(currentHour);

        let limit_num = BigNumber(dateLimit.getTime());
        let item_num = BigNumber(v.getTime());

        let diff = Number(limit_num.minus(item_num));

        if (diff < 0) {
          chartJSData.labels.push(item.datetime);
        }
      }
      chartJSData.datasets[1].data.push(item.price);
      chartJSData.datasets[1].pointBackgroundColor.push(
        "rgba(139, 68, 246, 0.9)"
      );
    });

    BTC_Prediction_VARMAX.forEach((item) => {
      chartJSData.datasets[2].data.push(item.price);
      chartJSData.datasets[2].pointBackgroundColor.push(
        "rgba(255, 166, 0, 0.9)"
      );
    });

    BTC_Prediction_SES.forEach((item) => {
      chartJSData.datasets[3].data.push(item.price);
      chartJSData.datasets[3].pointBackgroundColor.push(
        "rgba(33, 150, 243, 0.9)"
      );
    });

    BTC_Prediction_overall.forEach((item) => {
      chartJSData.datasets[4].data.push(item.price);
      chartJSData.datasets[4].pointBackgroundColor.push(
        "rgba(255, 98, 88, 0.9)"
      );
    });

    const legend = {
      labels: {
        usePointStyle: true,
        fontColor: "rgba(255, 255, 255, 0.7)",
      },
      position: "right",
    };
    const options = {
      maintainAspectRatio: false,
      responsive: true,
      title: {
        display: true,
        text: "Bitcoin Price",
        fontColor: "rgba(255, 255, 255, 0.7)",
      },
      tooltips: {
        mode: "label",
      },
      hover: {
        mode: "nearest",
        intersect: true,
      },
      scales: {
        xAxes: [
          {
            display: true,
            gridLines: {
              display: true,
              color: "rgba(255, 255, 255, 0.034)",
            },
            ticks: {
              fontColor: "rgba(255, 255, 255, 0.7)", // this here
            },
            scaleLabel: {
              display: true,
              labelString: "Time (30 min Window)",
              fontColor: "rgba(255, 255, 255, 0.7)",
            },
          },
        ],
        yAxes: [
          {
            display: true,
            gridLines: {
              display: true,
              color: "rgba(255, 255, 255, 0.034)",
            },
            ticks: {
              fontColor: "rgba(255, 255, 255, 0.7)", // this here
            },
            scaleLabel: {
              display: true,
              labelString: "Price (USD)",
              fontColor: "rgba(255, 255, 255, 0.7)",
            },
          },
        ],
      },
    };
    return (
      <div className="chartLine">
        <Line data={chartJSData} options={options} legend={legend} />
      </div>
    );
  }
}

export default BTPrice;
