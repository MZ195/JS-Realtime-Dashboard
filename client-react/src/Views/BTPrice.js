import React, { Component } from "react";
import { Line } from "react-chartjs-2";

class BTPrice extends Component {
  constructor() {
    super();
    this.state = {
      BTC_Data: [],
      BTC_Prediction_Data: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://localhost:9000/get_price/")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ BTC_Data: data });
        });
    }, 1700);

    setInterval(async () => {
      fetch("http://localhost:9000/predict/")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ BTC_Prediction_Data: data });
        });
    }, 1500);
  }

  render() {
    const { BTC_Data } = this.state;
    const { BTC_Prediction_Data } = this.state;

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
          label: "BTC Price Prediction",
          data: [],
          fontColor: "#fff",
          pointBackgroundColor: [],
          borderColor: "rgba(139, 68, 246, 0.9)",
          // fill: true,
          backgroundColor: "rgba(139, 68, 246, 0.03)",
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

    BTC_Prediction_Data.forEach((item) => {
      if (!chartJSData.labels.includes(item.datetime)) {
        chartJSData.labels.push(item.datetime);
      }
      chartJSData.datasets[1].data.push(item.price);
      chartJSData.datasets[1].pointBackgroundColor.push(
        "rgba(139, 68, 246, 0.9)"
      );
    });

    // var diff = A.filter((x) => !B.includes(x));

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
              labelString: "Time",
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
