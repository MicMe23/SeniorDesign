console.log("Hello world");
let data, cartesianGraph;

d3.csv('data/vector_matrix.csv')
  .then(_data => {
  	console.log('Data loading complete. Work with dataset.');
  	data = _data;
    console.log(data);

    //process the data - this is a forEach function.  You could also do a regular for loop.... 
    data.forEach(d => { //ARROW function - for each object in the array, pass it as a parameter to this function
      	// convert from strings to numbers
        d.magnitude = +d.magnitude;
        d.x_component = +d.x_component;
        d.y_component = +d.y_component;
        d.direction = +d.direction;
        d.x_location = +d.x_location;
        d.y_location = +d.y_location;
  	});

  	// Create an instance (for example in main.js)
		cartesianGraph = new CartesianGraph({
			'parentElement': '#timeline',
			'containerHeight': 1000,
			'containerWidth': 1000
		}, data);

})
.catch(error => {
    console.error('Error:');
    console.log(error);
});


/**
 * Event listener: use color legend as filter
 */
d3.selectAll('.legend-btn').on('click', function() {
  console.log("button! ");
  // Toggle 'inactive' class
  d3.select(this).classed('inactive', !d3.select(this).classed('inactive'));
  
  // Check which categories are active
  let selectedCategory = [];
  d3.selectAll('.legend-btn:not(.inactive)').each(function() {
    selectedCategory.push(d3.select(this).attr('category'));
  });

  // Filter data accordingly and update vis
  cartesianGraph.data = data.filter(d => selectedCategory.includes(d.category)) ;
  cartesianGraph.updateVis();

});

function computeDays(disasterDate){
  	let tokens = disasterDate.split("-");

  	let year = +tokens[0];
  	let month = +tokens[1];
  	let day = +tokens[2];

    return (Date.UTC(year, month-1, day) - Date.UTC(year, 0, 0)) / 24 / 60 / 60 / 1000 ;

  }