$(document).ready(function() {
    var svg = $('svg')[0];
    var width = svg.width.baseVal.value;
    var height = svg.height.baseVal.value;

    d3.select('svg')
        .selectAll('circle')
        .data(datasets[0])
        .enter()
        .append('circle')
            .attr('cx', function(d, i) {
                return (i+1) * 25;
            })
            .attr('cy', function(d) {
                // normalize to percentage scale
                return height - d / 100 * (height - 20) - 10;
            })
            .attr('r', 5)
            .attr('fill', '#6f96a2')
            .attr('stroke', 'white')
            .attr('stroke-width', 2);
});
