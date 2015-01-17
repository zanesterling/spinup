$(document).ready(function() {
    var svg = $('svg')[0];
    var width = svg.width.baseVal.value;
    var height = svg.height.baseVal.value;

    // add nodes for data
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

    // add lines between adjacent nodes
    d3.select('svg')
        .selectAll('circle')[0]
        .forEach(function(d, i, a) {
            // can't draw backwards from origin
            if (i == 0) return;

            // add a line from this node to the previous
            d3.select('svg')
                .append('line')
                    .attr('x1', d.cx.baseVal.value)
                    .attr('y1', d.cy.baseVal.value)
                    .attr('x2', a[i-1].cx.baseVal.value)
                    .attr('y2', a[i-1].cy.baseVal.value)
                    .attr('stroke', 'white')
                    .attr('stroke-width', 2);
        });
});
