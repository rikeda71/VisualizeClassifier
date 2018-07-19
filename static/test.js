function plotclassifier(sepline, vectors){

  Highcharts.chart('container', {
      xAxis: {
          min: -0.5,
          max: 5.5
      },
      yAxis: {
          min: 0
      },
      title: {
          text: 'Scatter plot with regression line'
      },
      series: [{
          type: 'line',
          name: 'Regression Line',
          data: [[0, 1.11], [5, 4.51]],
          marker: {
              enabled: false
          },
          states: {
              hover: {
                  lineWidth: 0
              }
          },
          enableMouseTracking: false
      }, {
          type: 'scatter',
          name: 'Observations',
          data: [[4.2, 3], [3, 5], [5, 1]],
          marker: {
              radius: 4
          }
      }]
  });

}
