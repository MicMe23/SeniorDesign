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

      vis.updateVis(); 
  }
}