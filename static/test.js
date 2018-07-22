function plotclassifier(sepline, vector){
  var [vecs, xmin, xmax, ymin, ymax]
      = arrange_vec(-sepline[0] / sepline[1], vector);
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
    series: vecs
  });
}

function arrange_vec(slope, input){
  $.ajaxSetup({ async: false });
  var vecs = [];
  var xmin, xmax, ymin, ymax;
  $.getJSON("static/test.json", function(json){
    xmin = Math.min.apply(null, json.vecs.x);
    xmax = Math.max.apply(null, json.vecs.x);
    ymin = xmin * slope;
    ymax = xmax * slope;
    /* 分離平面の設定 */
    const sepline = {
      type: 'line',
      name: 'Separation line',
      // ベクトルの最大値，最小値を活用
      data: [[xmin, ymin],
             [xmax, ymax]],
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
    /* 点ベクトルのフォーマット */
    // 入力テキストのベクトル
    var inputvec = {
      type: 'scatter',
      name: 'input sentence vector',
      data: [{
        x: input[0],
        y: input[1],
        text: 'sentence'
      }],
      color: 'rgba(80, 230, 80, 1)',
      marker: {
        radius: 6,
      },

    }
    // サンプルテキストのベクトル
    var pos = {
      type: 'scatter',
      name: 'positive',
      data: [],
      color: 'rgba(223, 83, 83, .8)',
      marker: {
        radius: 4,
      }
    }
    var neg = {
      type: 'scatter',
      name: 'negative',
      data: [],
      color: 'rgba(119, 120, 191, .8)',
      marker: {
        radius: 4,
      }
    }
    var obj
    // 点ベクトルをjsonから読み込んで用意
    for (var i = 0; i < json.sentences.length; ++i) {
      obj = {
        x: json.vecs.x[i],
        y: json.vecs.y[i],
        text: json.sentences[i]
      }
      // ネガポジで保存先を分岐
      if (json.sign[i] == 1) {
        pos.data.push(obj);
      }
      else {
        neg.data.push(obj);
      }
    }
    $.ajaxSetup({ async: true });
    // 可視化のパーツを1つずつ格納
    vecs.push(sepline);
    vecs.push(inputvec);
    vecs.push(pos);
    vecs.push(neg);
  });
  return [vecs, xmin, xmax, ymin, ymax];
}
