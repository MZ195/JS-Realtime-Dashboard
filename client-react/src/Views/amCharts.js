import React, { Component } from "react";
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
// import am4themes_dark from "@amcharts/amcharts4/themes/dark";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

// am4core.useTheme(am4themes_animated);
// Themes begin
// am4core.useTheme(am4themes_dark);
am4core.useTheme(am4themes_animated);
// Themes end

class TestAmCharts extends Component {
  constructor() {
    super();
    this.state = {
      PositiveTweetsData: [],
      NegativeTweetsData: [],
      myChartData: [],
    };
  }

  componentDidMount() {
    let chart = am4core.create("chartdiv", am4charts.XYChart);

    chart.paddingRight = 20;

    // const { PositiveTweetsData } = this.state;
    // const { NegativeTweetsData } = this.state;

    // let data = [];

    // PositiveTweetsData.forEach((item) => {
    //   chartJSData.labels.push(item.datetime);
    //   chartJSData.datasets[0].data.push(item.count);
    //   chartJSData.datasets[0].pointBackgroundColor.push(
    //     "rgba(0, 186, 156, 0.9)"
    //   );
    // });

    // let visits = 10;
    // for (let i = 1; i < 366; i++) {
    //   visits += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);
    // data.push({
    //   date: new Date(2018, 0, i),
    //   name: "name" + i,
    //   value: visits,
    // });
    // }

    let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.baseInterval = {
      timeUnit: "minute",
      count: 1,
    };
    // "HH:mm, d MMMM"
    // dateAxis.tooltipDateFormat = "Y-M-d H:m:s";

    let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.minWidth = 35;

    let series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "value";

    series.tooltipText = "{valueY.value}";
    chart.cursor = new am4charts.XYCursor();

    let scrollbarX = new am4charts.XYChartScrollbar();
    scrollbarX.series.push(series);
    chart.scrollbarX = scrollbarX;

    this.chart = chart;

    setInterval(async () => {
      fetch("http://localhost:9000/neg/")
        .then((res) => res.json())
        .then((res_data) => {
          var current_data = [];
          const { myChartData } = this.state;
          for (let i = 1; i < res_data.length; i++) {
            current_data.push({
              date: Date.parse(res_data[i].datetime),
              value: res_data[i].count,
            });
          }
          if (myChartData.length !== current_data.length) {
            this.chart.data = current_data;
            this.setState({ myChartData: current_data });
          }
        });
    }, 6000);
  }

  componentWillUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
  }

  render() {
    return <div id="chartdiv" style={{ width: "100%", height: "500px" }}></div>;
  }
}

export default TestAmCharts;
