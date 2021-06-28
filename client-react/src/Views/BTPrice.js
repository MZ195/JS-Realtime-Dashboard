import React, { Component } from "react";
import { Line } from "react-chartjs-2";

class BTPrice extends Component {
  constructor() {
    super();
    this.state = {
      BTC_Data: [],
      BTC_Prediction_ARIMA: [],
      BTC_Prediction_VARMAX: [],
      BTC_Prediction_SES: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      var v = new Date();
      if (
        v.getSeconds() === 32 ||
        v.getSeconds() === 2 ||
        v.getSeconds() === 10 ||
        v.getSeconds() === 40
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
      }
    }, 60);
  }

  render() {
    const { BTC_Data } = this.state;
    const { BTC_Prediction_ARIMA } = this.state;
    const { BTC_Prediction_VARMAX } = this.state;
    const { BTC_Prediction_SES } = this.state;

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
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(139, 68, 246, 0.9)",
          // fill: true,
          backgroundColor: "rgba(139, 68, 246, 0.03)",
        },
        {
          label: "BTC Price VARMAX",
          data: [],
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(255, 166, 0, 0.9)",
          // fill: true,
          backgroundColor: "rgba(255, 166, 0, 0.03)",
        },
        {
          label: "BTC Price SES",
          data: [],
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(33, 150, 243, 0.9)",
          // fill: true,
          backgroundColor: "rgba(33, 150, 243, 0.03)",
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

        if (v.getTime() > dateLimit.getTime()) {
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
