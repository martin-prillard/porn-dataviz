function displayGenericChart(file, chart_svg, cluster_color) {

      var chart = nv.models.discreteBarChart()
          .x(function(d) { return d.label })
          .y(function(d) { return d.value })
          .staggerLabels(true)
          .tooltips(false)
          .showValues(true)
          .showYAxis(false)
          .noData("");

        // add axis names
        // get info from title
        var re = /([a-z]+)_([a-z]+)/;
        var categorie = re.exec(file);

       if (categorie[2] == "views") {
            categorie[2] = "views (thousands)";
        }
        if (categorie[2] == "runtime") {
            categorie[2] = "runtime (minutes)";
        }

        chart.xAxis
                .axisLabel(categorie)
                .rotateLabels(-35)
                .tickFormat(d3.format('f'));

        d3.json("../dataset/generated/xhamster/json/histo_stat/" + file, function(json) {

            var data = json;

            historicalBarChart = new d3.range(0,1).map(function(d,i) { return {
              key: 'Stream' + i,
              values: data.map( function(f,j) {
                return {
                         "value": f.y,
                         "label": f.x
                       }
                    })
                };
            });

            nv.addGraph(function() {

              chartData = d3.select(chart_svg)
                  .datum(historicalBarChart)
                  .call(chart);

              // white text
              d3.selectAll('.nv-multiBarHorizontal text')
                .style('fill', "white");

              nv.utils.windowResize(chart.update);
              return chart;
            });

        });
     chart.color([cluster_color]);
     return chart;
}

redrawGraphStat = function(file, chart_svg, chart, cluster_color) {

    width = document.getElementById("containerNorth").getElementsByClassName("right")[0].offsetWidth;

    d3.json("../dataset/generated/xhamster/json/histo_stat/" + file, function(json) {

        var data = json;

        historicalBarChart = new d3.range(0,1).map(function(d,i) { return {
          key: 'Stream' + i,
          values: data.map( function(f,j) {
            return {
                     "value": f.y,
                     "label": f.x
                   }
                })
            };
        });

      chart.color([cluster_color])

      var re = /([a-z]+)_([a-z]+)/;
      var categorie = re.exec(file);

     if (categorie[2] == "views") {
        categorie[2] = "views (thousands)";
    }
    if (categorie[2] == "runtime") {
        categorie[2] = "runtime (minutes)";
    }

    d3.select(chart_svg).html("");

    d3.select(chart_svg)
        .datum(historicalBarChart)
        .call(chart)
        .append("text")
        .attr('x', width / 2)
        .attr('y', 30)
        .attr("text-anchor", "middle")
        .attr('class', 'chart-title')
        .style("fill", "white")
        .style("font-size", "15px")
        .text(categorie[2]);

      d3.select(chart_svg)
        .append("text")
        .attr('x', -85)
        .attr('y', 40)
        .attr("text-anchor", "middle")
        .attr('class', 'chart-title')
        .style("fill", "white")
        .style("font-size", "15px")
        .text("Number of videos")
        .attr('transform', function(d,i,j) { return 'rotate(-90,0,0)' });

      // white text
      d3.selectAll('.nv-multiBarHorizontal text')
              .style('fill', "white");
      nv.utils.windowResize(chart.update);
  });
};

function displayView(idCluster, chart) {
    var file = "nb_views_" + idCluster + ".json";
    redrawGraph(file, '#chart_view', chart);
}
function displayComment(idCluster, chart) {
    var file = "nb_comments_" + idCluster + ".json";
    redrawGraph(file, '#chart_comment', chart);
}
function displayDuration(idCluster, chart) {
    var file = "x_runtime_" + idCluster + ".json";
    redrawGraph(file, '#chart_runtime', chart);
}