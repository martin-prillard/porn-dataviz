  function displayCluster() {

      var colorBackground = "#292929";
      var clusterNull = 99;
      var colorClusterNull = "#e91aad";
      var idClusterSelected = -1;

      var widthCluster = document.getElementById("containerNorth").getElementsByClassName("left")[0].offsetWidth;
      var heightCluster = 600;

      var m = 20,
      radius = d3.scale.sqrt().range([0, 12]),
      color = d3.scale.category20().domain(d3.range(m));

      var clusters = new Array(m);

      var range_scale = d3.scale.ordinal()
          .domain(d3.range(46))
          .rangePoints([8, 25]);

      function getSizeText(r, text) {
          var len = text.length + 2;
          var size = r/3;
          size *= 10 / len;
          size += 1;
          return Math.round(size)
      }

      d3.json("../dataset/generated/xhamster/json/cluster/cluster_xhamster.json", function(json) {

          var nodes = json.nodes.map(function(node) {
              var i = node.group,
                  r = range_scale(node.degree),
                  label = censorship(node.tags),
                  ts = getSizeText(r, label),
                  d = {
                      tag: label,
                      cluster: node.group,
                      radius: r,
                      text_size: ts,
                      color: color(i),
                      x: Math.cos(i / m * 2 * Math.PI) * 200 + widthCluster / 2 + Math.random(),
                      y: Math.sin(i / m * 2 * Math.PI) * 200 + heightCluster / 2 + Math.random()
                  };
              clusters[i] = d;
              return d;
          });

          force = d3.layout.force()
              .nodes(nodes)
              .size([widthCluster, heightCluster])
              .on("tick", tick)
              .start();

          var svgCluster = d3.select("#cluster")
                  .append("svg")
                    .attr({
                  "width": widthCluster,
                  "height": heightCluster
           });

          var background = svgCluster.append("rect")
              .attr({
                  "width": widthCluster,
                  "height": heightCluster
              })
              .attr("fill", colorBackground)
              .on("click", function(d) {
                  var file = "nb_views_" + clusterNull + ".json";
                  redrawGraphStat(file, '#chart_view', chartview, colorClusterNull);
                  var file = "nb_comments_" + clusterNull + ".json";
                  redrawGraphStat(file, '#chart_comment', chartcomment, colorClusterNull);
                  var file = "x_runtime_" + clusterNull + ".json";
                  redrawGraphStat(file, '#chart_runtime', chartruntime, colorClusterNull);

                  updateWordCloud(clusterNull, myWordCloud);

                  d3.select('#chart_view').html("");
                  d3.select('#chart_comment').html("");
                  d3.select('#chart_runtime').html("");
                  d3.select('#chart_popularity').html("");
                  unSelectCluster();
              });

             var node = svgCluster.selectAll(".node")
              .data(nodes)
              .enter().append("g")
              .attr("class", "node");

              node.append("circle")
                  .attr("r", function(d) {return d.radius;})
                  .style("stroke", "black")
                  .style("stroke-width", 0.3)
                  .style("stroke-opacity", 0.5)
                  .style("fill", function(d) {return color(d.cluster);})

              node.append("text")
                  .attr("text-anchor", "middle")
                  .attr("font-family", "Comic Sans MS")
                  .attr("fill", "black")
                  .text(function(d) {return d.tag;})
                  .style("font-size", function(d) {return d.text_size + "px";})
                  .attr("dy", ".35em");

              node.on("click", function(d) { onMouseClick(d); })
                  .call(force.drag);

          var fisheye = d3.fisheye.circular()
                .radius(100);

         fisheyeMode = true;

         svgCluster.on("mousemove", function() {

            if (fisheyeMode) {

              fisheye.focus(d3.mouse(this));

              fisheye_effect(fisheye);
            }

        });

          function tick(e) {
               node.each(cluster(10 * e.alpha * e.alpha))
                       .each(collide(.5));
              fisheye_effect(fisheye);
          }

          function fisheye_effect(fisheye) {
            if (idClusterSelected > -1) {
                  svgCluster.selectAll(".node").filter(function(d) {
                      return d.cluster == idClusterSelected;
                  }).each(function() {
                      var n = d3.select(this);
                      n.select("circle")
                          .each(function(e) { e.fisheye = fisheye(e);})
                          .attr("transform", function(d) { return "translate(" + d.fisheye.x + "," + d.fisheye.y + ")";})
                          .attr("r", function(d) { return d.fisheye.z * d.radius;});
                      n.select("text")
                        .each(function(e) { e.fisheye = fisheye(e);})
                        .attr("transform", function(d) { return "translate(" + d.fisheye.x + "," + d.fisheye.y + ")";})
                        .style("font-size", function(d) {
                            return d.fisheye.z * d.text_size + "px";
                        });
                  });
                  svgCluster.selectAll(".node").filter(function(d) {
                      return d.cluster != idClusterSelected;
                  }).each(function() {
                      var n = d3.select(this);
                      n.select("circle")
                          .each(function(e) { e.fisheye = fisheye(e);})
                          .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")";})
                          .attr("r", function(d) { return d.radius;});
                      n.select("text")
                        .each(function(e) { e.fisheye = fisheye(e);})
                        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")";})
                        .style("font-size", function(d) {
                            return d.text_size + "px";
                        });
                  });
            } else {
               node.selectAll("circle").each(function(e) { e.fisheye = fisheye(e);})
                  .attr("transform", function(d) { return "translate(" + d.fisheye.x + "," + d.fisheye.y + ")";})
                  .attr("r", function(d) { return d.fisheye.z * d.radius;});

               node.selectAll("text").each(function(d) { d.fisheye = fisheye(d);})
                  .attr("transform", function(d) { return "translate(" + d.fisheye.x + "," + d.fisheye.y + ")";})
                  .style("font-size", function(d) {
                      return d.fisheye.z * d.text_size + "px";
                  });
            }
          }

          function cluster(alpha) {
              return function(d) {
                  var cluster = clusters[d.cluster];
                  if (cluster === d) return;
                  var x = d.x - cluster.x,
                      y = d.y - cluster.y,
                      l = Math.sqrt(x * x + y * y),
                      r = d.radius + cluster.radius;
                  if (l != r) {
                      l = (l - r) / l * alpha;
                      d.x -= x *= l;
                      d.y -= y *= l;
                      cluster.x += x;
                      cluster.y += y;
                  }
              };
          }

          padding = 33;
          // Resolves collisions between d and all other circles.
          function collide(alpha) {
              var quadtree = d3.geom.quadtree(nodes);
              return function(d) {
                  var r = d.radius + radius.domain()[1] + padding,
                      nx1 = d.x - r,
                      nx2 = d.x + r,
                      ny1 = d.y - r,
                      ny2 = d.y + r;
                  quadtree.visit(function(quad, x1, y1, x2, y2) {
                      if (quad.point && (quad.point !== d)) {
                          var x = d.x - quad.point.x,
                              y = d.y - quad.point.y,
                              l = Math.sqrt(x * x + y * y),
                              r = d.radius + quad.point.radius + (d.color !== quad.point.color) * padding;
                          if (l < r) {
                              l = (l - r) / l * alpha;
                              d.x -= x *= l;
                              d.y -= y *= l;
                              quad.point.x += x;
                              quad.point.y += y;
                          }
                      }
                      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
                  });
              };
          }

          var file = "nb_views_" + clusterNull + ".json";
          var chartview = displayGenericChart(file, '#chart_view', colorClusterNull);
          var file = "nb_comments_" + clusterNull + ".json";
          var chartcomment = displayGenericChart(file, '#chart_comment', colorClusterNull);
          var file = "x_runtime_" + clusterNull + ".json";
          var chartruntime = displayGenericChart(file, '#chart_runtime', colorClusterNull);
          var chartpopularity = displayPopularity(clusterNull);

       onMouseClick = function(d) {
          // is another node is selected
          if (d.cluster != idClusterSelected) {
              unSelectCluster();
              selectCluster(d);
              updateCharts(d.cluster, d.color);
          }
      };

      function updateCharts(idCluster, color_cluster) {
          var file = "nb_views_" + idCluster + ".json";
          redrawGraphStat(file, '#chart_view', chartview, color_cluster);
          var file = "nb_comments_" + idCluster + ".json";
          redrawGraphStat(file, '#chart_comment', chartcomment, color_cluster);
          var file = "x_runtime_" + idCluster + ".json";
          redrawGraphStat(file, '#chart_runtime', chartruntime, color_cluster);
          redrawGraphPopularity(idCluster, '#chart_popularity', chartpopularity);
      }

      function selectCluster(d) {

          document.getElementById("containerSouth").getElementsByClassName("left")[0].style.height = "400px";
          document.getElementById("containerSouth").getElementsByClassName("right")[0].style.height = "400px";

          // change global opacity
          node.style("opacity", 0.4);
          idClusterSelected = d.cluster;

          // resize cluster's node and label
          svgCluster.selectAll(".node").filter(function(d) {
              return d.cluster == idClusterSelected;
          }).each(function() {
              var n = d3.select(this).transition().duration(300).style("opacity", 1);
              n.select("circle")
                  .style("stroke-width", 2.5)
                  .style("stroke-opacity", 1)
          });

          onCluster = true;
      }

      function unSelectCluster() {

          document.getElementById("containerSouth").getElementsByClassName("left")[0].style.height = "0px";
          document.getElementById("containerSouth").getElementsByClassName("right")[0].style.height = "0px";

          // change global opacity
          node.style("opacity", 1);

          // resize last cluster's node and label
          if (idClusterSelected > -1) {
              svgCluster.selectAll(".node").filter(function(d) {
                  return d.cluster == idClusterSelected;
              }).each(function() {
                  var n = d3.select(this).transition().duration(300);
                  n.select("circle")
                      .style("stroke-width", 0.5)
                      .style("stroke-opacity", 0.5);
              });
          }

          idClusterSelected = -1;
      }

               });
}