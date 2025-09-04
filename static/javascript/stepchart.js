const sc_colorScale = d3.scaleOrdinal()
    .domain(["CORRECT", "INCORRECT", "HINT", null]) // null when there is no data
    .range(["#72DE90", "#F76F51", "#ffd68a", "#B0B0B0"]);
// process data and render heatmap
function renderStepChart(d, problemType, user, problem) {
    let allAttemptsData;
    if (d[problemType] && d[problemType][user] && d[problemType][user][problem]) {
        let data = d[problemType][user];
        allAttemptsData = data[problem];
    } else {
        allAttemptsData = [];
    }

    const newDate = new Date(1970, 01, 01, 0, 0, 0);

    let attempts = [];
    let selections = []; // steps in a problem. Here, in the order of student's attempts

    let timeElapsed = 0;
    for (let i = 0; i < allAttemptsData.length; i++) {
        
        let step = allAttemptsData[i];
        let entry = {};
        
        if (step.selection === "") {
            continue;
        } else {
            let startTime = timeElapsed;
            if (i == 0)
                timeElapsed = 0;
            else
                timeElapsed = timeElapsed + new Date(step.time).getTime()
                    - new Date(allAttemptsData[i - 1].time).getTime();
            entry.id = step.id;
            entry.correctness = step.correctness;
            entry.values = [{ selection: step.selection, time: new Date(newDate.getTime() + startTime) },
            { selection: step.selection, time: new Date(newDate.getTime() + timeElapsed) }];
            attempts.push(entry);

            // grey lines
            if (i + 1 < allAttemptsData.length) {
                entry = {};
                entry.correctness = null;
                entry.problem = step.problem
                entry.values = [
                    { selection: step.selection, time: new Date(newDate.getTime() + timeElapsed) },
                    { selection: allAttemptsData[i + 1].selection, time: new Date(newDate.getTime() + timeElapsed) }];
                attempts.push(entry);
            }

            // add "done" to the end of list
            if (!selections.includes(step.selection)) {
                selections.push(step.selection);
            }
        }
    }

    // bring the done and final_answer steps to the end
    if (selections.includes("done")) {
        let i = selections.findIndex(d => d == "done");
        selections.push(selections.splice(i, 1)[0]);
    }

    // show step chart
    //$('#stepchart').parents('div[class^="card"]').show();
    let parent = $('#stepchart').parents('.card');
    if (parent.is(":hidden"))
        $('#stepchart').parents('.card').show();

    createStepChart(attempts, selections, timeElapsed);
}

function createStepChart(attempts, selections, timeElapsed) {
    const sc_margin = { top: 50, right: 10, bottom: 50, left: 110 };
    const sc_width = $("#stepchart").parent().width() * 0.95 - sc_margin.left - sc_margin.right,
        sc_height = 450 - sc_margin.top - sc_margin.bottom;

    const svg = d3.select("#stepchart")
        .attr("width", sc_width + sc_margin.left + sc_margin.right)
        .attr("height", sc_height + sc_margin.top + sc_margin.bottom)

    const chart = svg.select('g.elements')
        .attr("transform", `translate(${sc_margin.left},${sc_margin.top})`);

    let x = d3.scaleTime().range([0, sc_width]);
    let y = d3.scalePoint().range([0, sc_height]).padding(0.25);

    let max = d3.max(attempts, d => d.values.at(-1).time);
    x.domain([d3.min(attempts, d => d.values[0].time), max]);

    let labelHt = 8; // includes padding

    const formatTimeMin = d3.timeFormat("%-M:%S");
    const formatTimeHR = d3.timeFormat("%H:%M:%S");
    //const formatTimeDay = d3.timeFormat("%-j:%H:%M:%S");

    let totalMinutes = Math.floor(timeElapsed / 1000 / 60);
    const formatTime = (totalMinutes > 60) ? formatTimeHR : formatTimeMin;
    let xAxis = d3.axisBottom(x).ticks(5).tickFormat(formatTime);

    let xAxisG = chart.select("g.x-axis")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${sc_height})`)
        .call(xAxis);
    y.domain(selections);

    // remove all contents within
    chart.select("g.y-axis").selectAll("*").remove();

    chart.select("g.y-axis")
        .call(d3.axisLeft(y))
        .attr("font-size", "9px")
        .attr("font-weight", "400");

    var line = d3.line()
        .x(d => x(d.time))
        .y(d => y(d.selection));
    d3.select('#line-clip rect')
        .attr('x', - 5)
        .attr('y', 0)
        .attr('width', sc_width + 10)
        .attr('height', sc_height);

    chart.select("g.lines")
        .selectAll(".sc_line")
        .data(attempts)
        .join("path")
        .attr("class", "sc_line")
        .attr("d", d => line(d.values))
        .attr("fill", "none")
        .attr("stroke", d => sc_colorScale(d.correctness))
        .attr("stroke-width", d => { if (!d.correctness) return 0.5; else return 6 })
        .attr("stroke-dasharray", (d) => { if (!d.correctness) return "0 4 0"; else return 0; })
        .attr('clip-path', 'url(#line-clip)')
        .on("mouseover", function (d, i) {
            toDatabase("hover", "stepchart", "");
        });

    // set back and grey labels
    let seenLabels = [];
    attempts.forEach(d => {
        if (!seenLabels.includes(d.values[0].selection)) {
            d3.select(`#sc_y_axis_${d.values[0].selection}`).attr('fill', 'black');
            seenLabels.push(d.values[0].selection);
        }
    });

    svg.select("text.title")
        .text(`Student: ${selectedStudent},  Question: ${selectedProblem}`)
        .attr("x", (sc_margin.left + sc_width + sc_margin.right) / 2)
        .attr("y", sc_margin.top * 0.25)
        .attr("dx", 0)
        .style("fill", 'black')
        .attr("text-anchor", "middle")
        .attr("font-size", "0.83em")
        .attr("font-weight", "500");

    let xLabel = (totalMinutes > 60) ? "Time (in hours)" : "Time (in minutes)";
    svg.select("text.x-label")
        .text(xLabel)
        .attr("x", (sc_margin.left + sc_width + sc_margin.right) / 2)
        .attr("y", sc_margin.top + sc_height + sc_margin.bottom * 0.75)
        .attr("dx", 0)
        .style("fill", 'black')
        .attr("text-anchor", "middle")
        .attr("font-size", "0.83em")
        .attr("font-weight", "500");

    svg.select("text.y-label")
        .text("Selections")
        .attr("x", sc_margin.left)
        .attr("y", sc_margin.top - 10)
        .style("fill", 'black')
        .attr("text-anchor", "end")
        .attr("font-size", "0.83em")
        .attr("font-weight", "500");

    // zoom
    function overViewZoom() {
        let t = d3.event.transform;
        /* let k = t.k / z.k;
        z = t; */

        // update x axis
        let newXScale = t.rescaleX(x);
        xAxisG.call(xAxis.scale(newXScale));

        // update line chart
        line.x(d => newXScale(d.time))
        chart.select("g.lines")
            .selectAll("path.sc_line")
            .attr("d", function (d) {
                if (d.values.length !== 0)
                    return line(d.values);
            });
    }

    let extent = [[0, 0], [sc_width, sc_height]];
    let chartZoom = d3.zoom()
        .translateExtent(extent)
        .extent(extent)
        .scaleExtent([1, 10000])
        .on('zoom', overViewZoom);

    svg.call(chartZoom);

    svg.on('click', function(e) {
        svg.transition()
          .duration(750)
          .call(chartZoom.transform, d3.zoomIdentity);
    })
}