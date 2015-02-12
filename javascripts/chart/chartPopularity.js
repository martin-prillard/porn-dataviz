function displayPopularity(idCluster) {

    //an example of harmonizing colors between visualizations
    //observe that Consumer Discretionary and Consumer Staples have
    //been flipped in the second chart
    var colors = d3.scale.category20();
    keyColor = function(d, i) {
        return colors(d.key)
    };

    var chart = nv.models.stackedAreaChart()
        .xScale(d3.time.scale())
        .useInteractiveGuideline(true)
        .x(function(d) {
            return d[0]
        })
        .y(function(d) {
            return d[1]
        })
        .color(keyColor)
        .transitionDuration(300)
        .noData("");

    chart.xAxis.tickFormat(function(d) {
        return d3.time.format('%Y')(new Date(d))
    }).ticks(d3.time.years);

    chart.yAxis.tickFormat(d3.format('%'));

    d3.json('../dataset/generated/xhamster/json/histo_popularity/cluster' + idCluster + '.json', function(data) {
        var histcatexplong = data;
        var histcatexpshort = data;

        nv.addGraph(function() {

            d3.select('#chart_popularity')
                .datum(histcatexplong)
                .transition().duration(1000)
                .call(chart)
                .transition().duration(0)
                .each('start', function() {
                    setTimeout(function() {
                        d3.selectAll('#chart_popularity *').each(function() {
                            if (this.__transition__)
                                this.__transition__.duration = 1;
                        })
                    }, 0)
                });
            nv.utils.windowResize(chart.update);
            return chart;
        });
    });
    return chart;
}

redrawGraphPopularity = function(idCluster, chart_svg, chart) {

    width = document.getElementById("containerSouth").getElementsByClassName("left")[0].offsetWidth;
    height = document.getElementById("containerSouth").getElementsByClassName("left")[0].offsetHeight;

    d3.json('../dataset/generated/xhamster/json/histo_popularity/cluster' + idCluster + '.json', function(data) {
        var histcatexplong = data;
        var histcatexpshort = data;

        //an example of harmonizing colors between visualizations
        //observe that Consumer Discretionary and Consumer Staples have
        //been flipped in the second chart
        var colors = d3.scale.category20();
        var keyColor = function(d, i) {
            return colors(d.key)
        };

        d3.select(chart_svg).html("");

        d3.select(chart_svg)
            .append("text")
            .attr("class", "y label")
            .attr("text-anchor", "middle")
            .attr('x', -height / 2)
            .attr('y', 10)
            .style("fill", "white")
            .style("font-size", "15px")
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .text("Proportion of tags among videos");

        d3.select(chart_svg)
            .append("text")
            .attr("class", "y label")
            .attr("text-anchor", "middle")
            .attr("x", width / 2)
            .attr("y", 390)
            .style("fill", "white")
            .style("font-size", "15px")
            .text("Popularity of tags over time");

        d3.select(chart_svg)
            .datum(histcatexplong)
            .transition().duration(1000)
            .call(chart)
            .transition().duration(0)
            .each('start', function() {
                setTimeout(function() {
                    d3.selectAll('#chart_popularity *').each(function() {
                        if (this.__transition__)
                            this.__transition__.duration = 1;
                    })
                }, 0)
            });

        censorshipPopularityGraph();

        nv.utils.windowResize(chart.update);
    });

};