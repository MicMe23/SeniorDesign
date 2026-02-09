class CartesianGraph {

  constructor(_config, _data) {
    this.config = {
      parentElement: _config.parentElement,
      containerWidth: _config.containerWidth || 1000,
      containerHeight: _config.containerHeight || 1000,
      margin: {top: 20, right: 20, bottom: 20, left: 20},
      tooltipPadding: _config.tooltipPadding || 15
    }

    this.data = _data; 

    this.initVis();
  }

    initVis() {
      //setting up the chart- things that won't need to update on user actions

      let vis = this; 
  

      // Width and height as the inner dimensions of the chart area- as before
      vis.width = vis.config.containerWidth - vis.config.margin.left - vis.config.margin.right;
      vis.height = vis.config.containerHeight - vis.config.margin.top - vis.config.margin.bottom;

      // Add <svg> element (drawing space)
      vis.svg = d3.select(vis.config.parentElement)
          .attr('width', vis.config.containerWidth)
          .attr('height', vis.config.containerHeight)

      vis.chart = vis.svg.append('g')
          .attr('transform', `translate(${vis.config.margin.left}, ${vis.config.margin.top})`);

      // Initialize linear scales
      vis.xScale = d3.scaleLinear()
        .domain([-20, 20])
        .range([0, vis.width]);

      vis.yScale = d3.scaleLinear()
        .domain([-20, 20]) 
        .range([vis.height, 0]);

      // ---- GRIDLINES ----
      // Draw gridlines from the chart bounds so they fill ALL quadrants

      vis.xGrid = d3.axisBottom(vis.xScale)
        .ticks(40)
        .tickSize(-vis.height)
        .tickFormat('');

      vis.xGridGroup = vis.chart.append('g')
        .attr('class', 'grid x-grid')
        .attr('transform', `translate(0, ${vis.height})`)
        .call(vis.xGrid);

      vis.yGrid = d3.axisLeft(vis.yScale)
        .ticks(40)
        .tickSize(-vis.width)
        .tickFormat('');

      vis.yGridGroup = vis.chart.append('g')
        .attr('class', 'grid y-grid')
        .attr('transform', `translate(0, 0)`)
        .call(vis.yGrid);

      // ---- AXES ----
      // Center the axes at (0,0) and draw them on top of the grid

      vis.xAxis = d3.axisBottom(vis.xScale);
      vis.yAxis = d3.axisLeft(vis.yScale);

      vis.xAxisGroup = vis.chart.append('g')
        .attr('class', 'axis x-axis') 
        .attr('transform', `translate(0, ${vis.yScale(0)})`)
        .call(vis.xAxis);

      vis.yAxisGroup = vis.chart.append('g')
        .attr('class', 'axis y-axis')
        .attr('transform', `translate(${vis.xScale(0)}, 0)`)
        .call(vis.yAxis);

      // ---- COLOR SCALE ----

      vis.colorScale = d3.scaleOrdinal(d3.schemeTableau10);

      vis.updateVis(); 
  }

  shortenLineForArrow(x1, y1, x2, y2, shortenPx) {
    let dx = x2 - x1;
    let dy = y2 - y1;
    let len = Math.sqrt(dx * dx + dy * dy);

    if (len === 0) {
      return { x2: x2, y2: y2 };
    }

    let ux = dx / len;
    let uy = dy / len;

    return {
      x2: x2 - ux * shortenPx,
      y2: y2 - uy * shortenPx
    };
}

  updateVis() {
    let vis = this;

    if (!vis.data || vis.data.length === 0) {
      return;
    }
    // ---- COLORED ARROWHEADS (one per vector) ----

    vis.defs = vis.svg.select('defs');
    if (vis.defs.empty()) {
      vis.defs = vis.svg.append('defs');
    }

    vis.colorScale.domain(d3.range(vis.data.length));

    vis.defs.selectAll('.arrowhead')
      .data(vis.data)
      .join('marker')
        .attr('class', 'arrowhead')
        .attr('id', (d, i) => `arrowhead-${i}`)
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 10)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
      .selectAll('path')
      .data((d, i) => [i])
      .join('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('fill', i => vis.colorScale(i));

    // Ensure stable colors by using index as the ordinal domain
    vis.colorScale.domain(d3.range(vis.data.length));

    // Group per vector (easy to extend later with labels, hover, etc.)
    vis.vectorGroups = vis.chart.selectAll('.vector')
      .data(vis.data)
      .join('g')
      .attr('class', 'vector');

    // Draw the vector shaft (from origin to origin + components)
    vis.vectorGroups.selectAll('line')
      .data((d, i) => [{ d: d, i: i }])
      .join('line')
      .attr('x1', p => vis.xScale(p.d.x_location))
      .attr('y1', p => vis.yScale(p.d.y_location))
      .attr('x2', p => {
        let x1 = vis.xScale(p.d.x_location);
        let y1 = vis.yScale(p.d.y_location);
        let x2 = vis.xScale(p.d.x_location + p.d.x_component);
        let y2 = vis.yScale(p.d.y_location + p.d.y_component);

        let shortened = vis.shortenLineForArrow(x1, y1, x2, y2, 10);
        return shortened.x2;
      })
      .attr('y2', p => {
        let x1 = vis.xScale(p.d.x_location);
        let y1 = vis.yScale(p.d.y_location);
        let x2 = vis.xScale(p.d.x_location + p.d.x_component);
        let y2 = vis.yScale(p.d.y_location + p.d.y_component);

        let shortened = vis.shortenLineForArrow(x1, y1, x2, y2, 10);
        return shortened.y2;
      })
      .attr('stroke', p => vis.colorScale(p.i))
      .attr('stroke-width', 2)
      .attr('marker-end', p => `url(#arrowhead-${p.i})`);


    // Label at the tip: A, B, C, ...
    vis.vectorGroups.selectAll('text')
      .data((d, i) => [{ d: d, i: i }])
      .join('text')
      .attr('x', p => vis.xScale(p.d.x_location + p.d.x_component) + 6)
      .attr('y', p => vis.yScale(p.d.y_location + p.d.y_component) - 6)
      .text(p => String.fromCharCode(65 + p.i))
      .attr('font-size', 12)
      .attr('fill', p => vis.colorScale(p.i));
  }

}
