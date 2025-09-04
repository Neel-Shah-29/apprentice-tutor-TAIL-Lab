function processHeatmapData(d) {
	let problem_types = Object.keys(d);
	let students = new Set();
	let heatMapData = [];

	for (let p of problem_types) {
		let students_attempted = Object.keys(d[p]);

		for (let i = 0; i < students_attempted.length; i++) {
			let entry = {};
			entry.problem_type = p;

			let s = students_attempted[i];

			students.add(s);

			entry.student = s;
			entry.attempt_count = Object.keys(d[p][s]).length;
			heatMapData.push(entry);
		}
	}

	return [Array.from(students), problem_types, heatMapData];
}

function formatData(data) {
	let problems = Object.keys(data);
	let students = [];
	let heatMapData = [];

	for (let problem of problems) {
		let entry = {};
		entry.problem = problem;
		for (let student of Object.keys(data[problem])) {
			entry.student = student;
			students.push(student);

			let lastStep = data[problem][student].at(-1);

			entry.problemScore = (lastStep.selection == "done" && lastStep.correctness == "CORRECT") ? 1 : 0;
			heatMapData.push(entry);
		}
	}
	return [students, heatMapData];
}

function formatDummyData(data) {
	problems = [];
	students = [];
	// data = {'A': {'s1': []}, 'B': {'s1': [], 's2': []}}

	data.forEach(entry => {
		if (!problems.includes(entry.problem))
			problems.push(entry.problem);
		if (!students.includes(entry.student))
			students.push(entry.student);
	});
}

// process data and render heatmap
function renderHeatmap(data) {

	console.log("heatmap");

	// let colorScheme = {"hint": "#ffd68a",
 //                    "incorrect": "#d7191c",
 //                    "correct": "#a6d96a",
 //                    "null": "#bdbdbd"};

	let problems = Object.keys(data);
	let [students, problem_types, heatMapData] = processHeatmapData(data);

	let cellHeight = 10;

	let canvas = {"height": problems.length * cellHeight + 75,
		          "width": $("#heatmap").parent().width() * 0.95,
		          "marginLeft": 120,
		          "marginTop": 50,
		          "marginRight": 20,
		          "marginBottom": 25}

	let cellWidth = (canvas.width - canvas.marginLeft - canvas.marginRight) / students.length;

	const opacityScale = d3.scaleLinear()
		.domain(d3.extent(heatMapData, x => x.attempt_count))
		.range([0.5, 1]);

	// heatmap constants
	// const cellHt = 15;
	// const cellWd = 20;
	// const cellPadding = 0.02;


	const svg = d3.select("#heatmap")
		.attr("width", canvas.width)
		.attr("height", canvas.height);

	// Build X scales and axis:
	const xScale = d3.scaleBand()
		.domain(students)
		.range([canvas.marginLeft, canvas.width - canvas.marginRight]);

	// const yScale = d3.scaleLinear()
	// 	.domain([1, problems.length + 1])
	// 	.range([canvas.marginTop, canvas.height - canvas.marginBottom])

	const yScale = d3.scaleBand()
		.domain(problem_types)
		.range([canvas.marginTop, canvas.height-canvas.marginBottom]); // list of all students who attempted all questions

	svg.selectAll(".cell")
		.data(heatMapData)
		.join("rect")
		.attr("class", "cell")
		.attr("x", d => xScale(d.student))
		.attr("y", d => yScale(d.problem_type))
		.attr("width", cellWidth)
		.attr("height", cellHeight)
		.attr("fill", "#4e79a7")
		.attr("opacity", d => opacityScale(d.attempt_count));


	svg.selectAll(".problem")
		.data(problem_types)
		.join("text")
		.attr("class", "problem")
		.text(d => d)
		.attr("x", 10)
		.attr("y", d => yScale(d) + 2)
		.attr("alignment-baseline", "hanging")
		.attr("font-size", 8);

	svg.selectAll(".student")
		.data(students)
		.join("text")
		.attr("class", "student")
		.text(d => d)
		.attr("font-size", 8)
		.attr("transform", d => `translate(${xScale(d)}, 10) rotate(-45)`)
		.attr("text-anchor", "middle");

	// chart.append("g")
	// 	.call(d3.axisTop(x))
	// 	.attr('stroke-opacity', 0)
	// 	.style('font-size', "0.7em")
	// 	.selectAll("text")
	// 	.attr("transform", "translate(5,0) rotate(-45)")
	// 	.attr("text-anchor", "start");

	// Build X scales and axis:

	// chart.append("g")
	// 	.call(d3.axisLeft(y))
	// 	.attr('stroke-opacity', 0)
	// 	.style('font-size', "0.7em");

	// chart.selectAll()
	// 	//.data(heatMapData)
	// 	.data(data)
	// 	/* .data(data, function (d) { 
	// 		return d.group + ':' + d.variable;
	// 	 }) */
	// 	.join("rect")
	// 	.attr("x", function (d) {
	// 		return x(d.problem);
	// 		//return x(d.group);
	// 	})
	// 	.attr("y", function (d, i) {
	// 		//return cellHt * i;
	// 		return y(d.student);
	// 	})
	// 	.attr("width", x.bandwidth())
	// 	.attr("height", y.bandwidth())
	// 	.style("fill", function (d) { return colorScale(d.problemScore) })
}

function createHeatMap() {

}