function plotclassifier(sepline, vectors){
  vecs = arrange_vec();
  vecs.unshift(
    {
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
    }
  )
  Highcharts.chart('container', {
    xAxis: {
      title: {
        enabled: true,
        text: 'positive condition'
      },
      min: -0.5,
      max: 5.5
    },
    yAxis: {
      title: {
        enabled: true,
        text: 'negative condition'
      },
      min: 0
    },
    title: {
      text: 'Scatter plot with regression line'
    },
    tooltip: {
      pointFormat: 'text: {point.text}<br>x: {point.x}<br>y: {point.y}',
    },
    series: vecs
  });
}

function arrange_vec(){
  $.ajaxSetup({ async: false });
  var vecs = []
  $.getJSON("static/test.json", function(json){
    var pos = {
      type: 'scatter',
      name: 'positive',
      data: [],
      color: 'rgba(223, 83, 83, .5)',
      marker: {
        radius: 4,
      }
    }
    var neg = {
      type: 'scatter',
      name: 'negative',
      data: [],
      color: 'rgba(119, 120, 191, .5)',
      marker: {
        radius: 4,
      }
    }
    const len = json.sentences.length;
    var obj
    for (var i = 0; i < len; ++i) {
      obj = {
        x: json.vecs.x[i],
        y: json.vecs.y[i],
        text: json.sentences[i]
      }
      if (json.sign[i] == 1) {
        pos.data.push(obj);
      }
      else {
        neg.data.push(obj);
      }
    }
    $.ajaxSetup({ async: true });
    vecs.push(pos);
    vecs.push(neg);
  });
  return vecs
}
