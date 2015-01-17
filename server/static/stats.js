$(document).ready(function() {
    d3.select('svg')
        .selectAll('circle')
        .data(datasets[0])
        .enter()
        .append('circle')
            .attr('cx', function(d, i) {
                return (i+1) * 25;
            })
            .attr('cy', function(d) {
                return d * 25;
            })
            .attr('r', 5)
            .attr('fill', 'blue')
            .attr('stroke', 'gray')
            .attr('stroke-width', 2);
});
