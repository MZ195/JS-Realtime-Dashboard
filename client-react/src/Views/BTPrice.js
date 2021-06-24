import React, { Component } from "react";
import { Line } from "react-chartjs-2";

class BTPrice extends Component {
  constructor() {
    super();
    this.state = {
      myChartData: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://localhost:9000/get_price/")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ myChartData: data });
        });
    }, 30000);
  }

  render() {
    const { myChartData } = this.state;

    // var canvas = document.getElementById("lineChart");
    // var ctx = canvas.getContext("2d");

    // var gradientFill = ctx.createLinearGradient(0, 0, 0, 290);
    // gradientFill.addColorStop(0, "rgba(173, 53, 186, 1)");
    // gradientFill.addColorStop(1, "rgba(173, 53, 186, 0.1)");

    let chartJSData = {
      labels: [],
      datasets: [
        {
          label: "BT Price",
          data: [],
          pointBackgroundColor: [],
          borderColor: "rgba(255, 193, 7, 0.9)",
          fill: false,
        },
      ],
    };

    myChartData.forEach((item) => {
      chartJSData.labels.push(item.datetime);
      chartJSData.datasets[0].data.push(item.price);
      chartJSData.datasets[0].pointBackgroundColor.push(
        "rgba(255, 193, 7, 0.9)"
      );
    });

    const legend = {
      labels: {
        usePointStyle: true,
      },
      position: "right",
    };
    const options = {
      maintainAspectRatio: false,
      responsive: true,
      title: {
        display: true,
        text: "Bitcoin Price",
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
            },
            scaleLabel: {
              display: true,
              labelString: "Time",
            },
          },
        ],
        yAxes: [
          {
            display: true,
            gridLines: {
              display: true,
            },
            scaleLabel: {
              display: true,
              labelString: "Price (USD)",
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
