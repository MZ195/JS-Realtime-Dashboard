import React, { Component } from "react";
import { Radar } from "react-chartjs-2";

class DailyTweetsRadar extends Component {
  constructor() {
    super();
    this.state = {
      myChartData: [],
    };
  }

  componentDidMount() {
    // setInterval(async () => {
    fetch("http://localhost:9000/tweets/daily")
      .then((res) => res.json())
      .then((data) => {
        this.setState({ myChartData: data });
      });
    // }, 30000);
  }

  render() {
    const { myChartData } = this.state;

    let chartJSData = {
      labels: [],
      datasets: [
        {
          label: "Positive Tweets",
          data: [],
          fill: true,
          backgroundColor: "rgba(0, 186, 156, 0.5)",
          // borderColor: "rgb(0, 186, 156)",
          // pointBackgroundColor: "rgb(0, 186, 156)",
          // pointBorderColor: "#000",
          // pointHoverBackgroundColor: "#000",
          // pointHoverBorderColor: "rgb(0, 186, 156)",
        },
        {
          label: "Negative Tweets",
          data: [],
          fill: true,
          backgroundColor: "rgba(230, 73, 84, 0.5)",
          // borderColor: "rgb(230, 73, 84)",
          // pointBackgroundColor: "rgb(230, 73, 84)",
          // pointBorderColor: "#000",
          // pointHoverBackgroundColor: "#000",
          // pointHoverBorderColor: "rgb(230, 73, 84)",
        },
      ],
    };

    myChartData.forEach((item) => {
      chartJSData.labels.push(item.datetime);
      chartJSData.datasets[0].data.push(item.pos);
      chartJSData.datasets[1].data.push(item.neg);
    });

    const legend = {
      display: false,
      position: "top",
      labels: {
        fontColor: "#000",
      },
    };
    const options = {
      responsive: true,
      title: {
        display: true,
        text: "Today's Tweets Analysis",
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
      // scales: {
      //   xAxes: [
      //     {
      //       display: true,
      //       gridLines: {
      //         display: true,
      //       },
      //       scaleLabel: {
      //         display: true,
      //         labelString: "Time",
      //       },
      //     },
      //   ],
      //   yAxes: [
      //     {
      //       display: true,
      //       gridLines: {
      //         display: true,
      //       },
      //       scaleLabel: {
      //         display: true,
      //         labelString: "Count",
      //       },
      //     },
      //   ],
      // },
    };
    return (
      <div className="my-auto mx-auto chartjs-render-monitor">
        <Radar data={chartJSData} options={options} legend={legend} />
      </div>
    );
  }
}

export default DailyTweetsRadar;
