import React, { Component } from "react";
import { Polar } from "react-chartjs-2";

class DailyTweetsRadar extends Component {
  constructor() {
    super();
    this.state = {
      myChartData: [],
    };
  }

  componentDidMount() {
    setInterval(async () => {
      fetch("http://127.0.0.1:9000/tweets/count")
        .then((res) => res.json())
        .then((data) => {
          this.setState({ myChartData: data });
        });
    }, 30000);
  }

  render() {
    const { myChartData } = this.state;

    let chartJSData = {
      labels: ["Positive", "Negative"],
      datasets: [
        {
          label: "Today's Tweets",
          data: [myChartData["Total_pos"], myChartData["Total_neg"]],
          fill: true,
          backgroundColor: [
            "rgba(68, 168, 184, 0.9)",
            "rgba(139, 68, 246, 0.9)",
          ],
        },
      ],
    };

    const legend = {
      display: false,
      position: "top",
      labels: {
        fontColor: "rgba(255, 255, 255, 0.7)",
      },
    };
    const options = {
      maintainAspectRatio: false,
      responsive: true,
      title: {
        display: true,
        text: "Today's Tweets Analysis",
        fontColor: "rgba(255, 255, 255, 0.7)",
      },
      tooltips: {
        mode: "label",
      },
      hover: {
        mode: "nearest",
        intersect: true,
      },
      elements: {
        point: {
          radius: 0,
        },
      },
    };
    return (
      <div className="my-auto mx-auto radar-chart chartjs-render-monitor">
        <Polar data={chartJSData} options={options} legend={legend} />
      </div>
    );
  }
}

export default DailyTweetsRadar;
