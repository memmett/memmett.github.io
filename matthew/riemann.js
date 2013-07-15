var w = 600;
var h = 400;

var svg = d3.select("div#riemann").append("svg:svg").attr("width", w).attr("height", h);

//var N    = 10;			// number of riemann rectangles
var Npt  = 50;			// number of graph points
var xmin = -1;
var xmax =  1;
var ymin =  -0.5;
var ymax =  2.0;
var pad  =  30;

var x = d3.scale.linear().range([pad/2, w-pad/2]).domain([xmin, xmax]),
    y = d3.scale.linear().range([h-pad/2, pad/2]).domain([ymin, ymax]);


function f(d) {
  return 1 + 8*d*d*d/10;
}

function draw_rects(N, alpha) {
    var xi  = d3.range(xmin, xmax-1e-9, (xmax-xmin)/N);
    var dx  = (x(xmax) - x(xmin)) / N;
    var adj = alpha * (xmax - xmin) / N; 
    var rect = svg.selectAll("rect").data(xi).enter().append("rect")
	.attr("x", function(d) { return x(d); })
	.attr("y", function(d) { return y(f(d+adj)); })
	.attr("width", function(d) { return dx; })
	.attr("height", function(d) { return y(0)-y(f(d+adj)); })
	.attr("class", "rrect");
}

var n = document.getElementById('n-input').value;
var a = document.getElementById('a-input').value;
draw_rects(n, a);

function riemann(n, a) {
  var r = 0.0;
  var dx  = (xmax - xmin) / n;
  for (var i=0; i<n; i++) {
    r += f(xmin + (i+a)*dx);
  }
  return r * dx;
}

function update() {
    var n = document.getElementById('n-input').value;
    var a = document.getElementById('a-input').value;

    svg.selectAll(".rrect").data([]).exit().remove()

    // var lsvg = d3.select("body").transition();

    // lsvg.select(".line")   // change the line
    //         .duration(750)
    //         .attr("d", valueline(data));
    //     svg.select(".x.axis") // change the x axis
    //         .duration(750)
    //         .call(xAxis);
    //     svg.select(".y.axis") // change the y axis
    //         .duration(750)
    //         .call(yAxis);

    d3.select("#n-value").text(n);
    d3.select("#a-value").text(a);
    draw_rects(n, a);

    d3.select("#ra-value").text(riemann(n, parseFloat(a)).toFixed(3));
    // d3.select("#r0-value").text(riemann(n, 0.0));
    // d3.select("#r1-value").text(riemann(n, 1.0));
}


// draw the x axis

var xaxis = d3.svg.axis().scale(x).orient("bottom");
svg.append("g").attr("id", "xaxis").attr("transform", "translate(0," + (h - pad) + ")").call(xaxis);

// draw the graph

var graph = d3.svg.line()
    .x(function(d) { return x(d); })
    .y(function(d) { return y(f(d)); })
    .interpolate("basis");

var xi = d3.range(xmin, xmax+1e-9, (xmax-xmin)/Npt);
svg.append("path").attr("id", "graph").attr("d", graph(xi));

update();
