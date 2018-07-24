var cnt = 0;
var id = null;

function plotting() {
  if (document.auto.auto.checked) {
    if (id == null)
      id = setInterval(plottraining, 2000);
  }
  else {
    stop_plotting()
    plottraining();
  }
}

function stop_plotting() {
  if (id != null) {
    clearInterval(id);
    id = null
  }
}

function plottraining() {
  var [vecs, xmin, xmax, ymin, ymax] = formatting_marker_in_train_data();
  Highcharts.chart('container', {
    xAxis: {
      title: {
        enabled: true,
        text: 'positive condition'
      },
      min: xmin,
      max: xmax
    },
    yAxis: {
      title: {
        enabled: true,
        text: 'negative condition'
      },
      min: ymin,
      max: ymax
    },
    title: {
      text: 'Separation line and vectors of sentence in vector space'
    },
    tooltip: {
      pointFormat: 'text: {point.text}<br>x: {point.x}<br>y: {point.y}',
    },
    plotOptions: {
      series: {
        animation: false
      }
    },
    series: vecs
  });
}

function formatting_marker_in_train_data() {
  var vecs = []
  var xmin, xmax, ymin, ymax;
  $.ajaxSetup({ async: false });
  $.getJSON("static/json/" + cnt.toString() +".json", function(json){
    const slope = -json.line.x / json.line.y;
    xmin = 0, xmax = 5, ymin = xmin, ymax = xmax * slope;
    const sepline = {
      type: 'line',
      name: 'Separation line',
      data: [[xmin, ymin],
        [xmax, ymax]],
      marker: {
        enabled: false
      },
      status: {
        hover: {
          lineWidth: 0
        }
      },
      enableMouseTracking: false
    };
    const beforeline = {
      type: 'line',
      name: 'Separation line before one step',
      data: [[xmin, ymin],
        [xmax, xmax * -json.bline.x / json.bline.y]],
      marker: {
        enabled: false
      },
      status: {
        hover: {
          lineWidth: 0
        }
      },
      enableMouseTracking: false
    };
    /* 点ベクトルのフォーマット */
    var pos = {
      type: 'scatter',
      name: 'positive',
      data: [],
      color: 'rgba(223, 83, 83, .8)',
      marker: {
        radius: 4,
      }
    };
    var neg = {
      type: 'scatter',
      name: 'negative',
      data: [],
      color: 'rgba(119, 120, 191, .8)',
      marker: {
        radius: 4,
      }
    };
    const len = json.vec.length;
    const c = json.vec[len-1].sign == 1 ? 'rgba(250, 50, 50, 1)' : 'rgba(50, 50, 250, 1)'
    var current = {
      type: 'scatter',
      name: 'current',
      data: [{
        x: json.vec[len - 1].x,
        y: json.vec[len - 1].y,
        text: json.vec[len - 1].text
      }],
      color: c,
      marker: {
        symbol: 'circle',
        radius: 7,
      }
    };
    for (var i = 0; i < len - 1; ++i) {
      obj = {
        x: json.vec[i].x,
        y: json.vec[i].y,
        text: json.vec[i].text
      };
      if (json.vec[i].sign == 1) {
        pos.data.push(obj);
      }
      else {
        neg.data.push(obj);
      }
    }
    $.ajaxSetup({ async: true });
    // 可視化のパーツを1つずつ格納
    vecs.push(sepline);
    vecs.push(beforeline);
    vecs.push(pos);
    vecs.push(neg);
    vecs.push(current);
  });
  cnt++;
  return [vecs, xmin, xmax, -5, 30];
}
