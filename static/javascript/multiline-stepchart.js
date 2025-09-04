var interfaceSelections;
let ml_zoom = d3.zoomIdentity;
function renderMultiLineStepChart(d, problemType, student = "all") {
    const newDate = new Date(1970, 01, 01, 0, 0, 0);

    let dynamicList;
    let ml_attempts = []; // reset list

    let selections = []; // steps in a problem -- in the order of user's attempts

    let maxTimeElapsed = 0;
    // problems attempted by one user, for multiple questions
    for (let user of Object.keys(d[problemType])) { // each user
        userProblems = d[problemType][user]; // all problems attempted by user

        if (student != "all" && user != student) {
            continue
        }

        for (let j = 0; j < Object.keys(userProblems).length; j++) { // each problem
            let que = Object.keys(userProblems)[j];
            let queAttempts = userProblems[que];

            let entry = { id: que, user: user, values: [] }; // all questions in the unique interface
            let timeElapsed = 0;
            for (let i = 0; i < queAttempts.length; i++) {
                // CHECK: will all entries be input change?
                let step = queAttempts[i];

                //if (step.action === "start new problem") {
                //if (i === 0) {
                if (step.selection == "") {
                    continue;
                } else {
                    let startTime = timeElapsed;
                    timeElapsed = timeElapsed + new Date(step.time).getTime()
                        - new Date(queAttempts[i - 1].time).getTime();
                    // values will hold the line data for a user
                    if (entry.values.length != 0) {
                        entry.values.push({ selection: step.selection, time: new Date(newDate.getTime() + startTime) },
                            { selection: step.selection, time: new Date(newDate.getTime() + timeElapsed) });
                    } else {
                        entry.values = [{ selection: step.selection, time: new Date(newDate.getTime() + startTime) },
                        { selection: step.selection, time: new Date(newDate.getTime() + timeElapsed) }];
                    }
                    // add "done" to the end of list
                    if (j == 0 && !selections.includes(step.selection)) {
                        selections.push(step.selection);
                    }

                    if (j != 0 && !selections.includes(step.selection)) {
                        selections.push(step.selection);
                    }
                }
            }
            maxTimeElapsed = timeElapsed > maxTimeElapsed ? timeElapsed : maxTimeElapsed;
            ml_attempts.push(entry);
        }
        // hide step chart for the new multi-line chart
        $('#stepchart').parents('.card').hide();
    }
    // bring the done and final_answer steps to the end
    if (selections.includes("done")) {
        let i = selections.findIndex(d => d == "done");
        selections.push(selections.splice(i, 1)[0]);
    }

    let has_attempts = (ml_attempts.filter(a => a.values.length > 0)).length;

    if (has_attempts > 0) {
        createMultiLineStepChart2(ml_attempts, selections, maxTimeElapsed);
    } else {
        createError(student);
    }
    
}

function createError(student) {

    const ml_margin = { top: 0, right: 10, bottom: 0, left: 110 };
    const ml_width = $("#multiline-stepchart").parent().width() * 0.95 - ml_margin.left - ml_margin.right,
        ml_height = 50;

    d3.select("#multiline-stepchart").attr("height", 0);

    const svg = d3.select("#multiline-error")
        .attr("width", ml_width + ml_margin.left + ml_margin.right)
        .attr("height", ml_height + ml_margin.top + ml_margin.bottom);

    svg.selectAll("text")
        .data([`student ${student} has not attempted this problem type`])
        .join("text")
        .attr("x", ml_margin.left)
        .attr("y", ml_height/2)
        .attr("text-anchor", "start")
        .attr("alignment-baseline", "middle")
        .text(d => d);

}

function createMultiLineStepChart2(ml_attempts, selections, maxTimeElapsed) {
    const ml_margin = { top: 50, right: 10, bottom: 50, left: 110 };
    const ml_width = $("#multiline-stepchart").parent().width() * 0.95 - ml_margin.left - ml_margin.right,
          ml_height = 450 - ml_margin.top - ml_margin.bottom;

    d3.select("#multiline-error").attr("height", 0);

    const svg = d3.select("#multiline-stepchart")
        .attr("width", ml_width + ml_margin.left + ml_margin.right)
        .attr("height", ml_height + ml_margin.top + ml_margin.bottom);

    // Tooltip setup
    let tooltip = d3.select("#tooltip");
    if (tooltip.empty()) {
        tooltip = d3.select("body") 
            .append("div")
            .attr("id", "tooltip")
            .style("position", "absolute")
            .style("visibility", "hidden")
            .style("z-index", "9999") 
            .style("font-size", "10px")
            .style("border", "solid 1px black")
            .style("border-radius", "4px")
            .style("padding", "5px")
            .style("background-color", "white");
    }

    const chart = svg.select("g.elements")
        .attr("transform", `translate(${ml_margin.left},${ml_margin.top})`);

    const formatTimeMin = d3.timeFormat("%-M:%S");
    const formatTimeHR = d3.timeFormat("%H:%M:%S");

    let x = d3.scaleTime().range([0, ml_width]);
    let y = d3.scalePoint().range([0, ml_height]).padding(0.25);

    let totalMinutes = Math.floor(maxTimeElapsed / 1000 / 60);
    const formatTime = (totalMinutes > 60) ? formatTimeHR : formatTimeMin;
    let xAxis = d3.axisBottom(x).tickFormat(formatTime).ticks(7);

    let max = d3.max(ml_attempts, d => d.values.length ? d.values.at(-1).time : null);

    x.domain([new Date(1970, 1, 1, 0, 0, 0).getTime(), max]);
    y.domain(selections);

    chart.select("g.x-axis")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${ml_height})`)
        .call(xAxis);

    chart.select("g.y-axis").selectAll("*").remove();
    chart.select("g.y-axis")
        .call(
            d3.axisLeft(y).tickFormat(d => {
                let text = (d ?? "").toString().replace(/<[^>]*>/g, "").trim();
                let maxLen = 20;
                return text.length > maxLen ? text.slice(0, maxLen) + "..." : text;
            })
        )
        .attr("font-size", "9px")
        .attr("font-weight", "400")
        .selectAll(".tick text")
        .append("title")
        .text(d => (d ?? "").toString().replace(/<[^>]*>/g, "").trim());

    let line = d3.line()
        .x(d => x(d.time))
        .y(d => y(d.selection));

    d3.select('#multiline-clip rect')
        .attr('x', -5)
        .attr('y', 0)
        .attr('width', ml_width + 10)
        .attr('height', ml_height);

    let mainlines = chart.select("g.lines")
        .selectAll(".main_multiline")
        .data(ml_attempts, d => d.id)
        .join("path")
        .attr("id", (d, i) => `mainline-${d.user}-${i}`)
        .attr("class", "main_multiline")
        .attr("d", d => d.values.length ? line(d.values) : null)
        .attr("fill", "none")
        .attr("stroke-width", 2)
        .attr("opacity", 0.6)
        .attr("stroke", "#79DCFF");

    chart.select("g.lines")
        .selectAll(".hidden_multiline")
        .data(ml_attempts, d => d.id)
        .join("path")
        .attr("id", (d, i) => `hiddenline-${d.user}-${i}`)
        .attr("class", "hidden_multiline")
        .attr("d", d => d.values.length ? line(d.values) : null)
        .attr("fill", "none")
        .attr("opacity", 0)
        .attr("stroke", "black")
        .attr("stroke-width", "5px")
        .attr('clip-path', 'url(#multiline-clip)')
        .attr("cursor", "pointer")
        .on("mouseover", function (event, i) {
            toDatabase("hover", "multiline", i.user);
            mainlines.attr('opacity', 0.6);
            mainlines.filter(md => md.id === i.id).attr('opacity', 1);

            let firstValue = i.values[0];
            let lastValue = i.values.at(-1);
            let durationMs = lastValue.time - firstValue.time;
            let durationSec = Math.floor(durationMs / 1000);
            let durationStr = `${Math.floor(durationSec / 60)}m ${durationSec % 60}s`;

            tooltip
                .style("visibility", "visible")
                .style("left", `${event.pageX + 15}px`)
                .style("top", `${event.pageY + 15}px`)
                .html(
                    `<strong>User:</strong> ${i.user}<br>
                     <strong>First Selection:</strong> ${firstValue.selection}<br>
                     <strong>Start Time:</strong> ${formatTime(firstValue.time)}<br>
                     <strong>End Time:</strong> ${formatTime(lastValue.time)}<br>
                     <strong>Duration:</strong> ${durationStr}`
                );
        })
        .on("mousemove", function (event) {
            tooltip
                .style("left", `${event.pageX + 15}px`)
                .style("top", `${event.pageY + 15}px`);
        })
        .on("mouseout", function () {
            mainlines.attr('opacity', 0.6);
            tooltip.style("visibility", "hidden");
        });

    // Labels
    svg.select("text.title")
        .text(`Question Type: ${selectedProblemType}`)
        .attr("x", (ml_margin.left + ml_width + ml_margin.right) / 2)
        .attr("y", ml_margin.top * 0.25)
        .style("fill", 'black')
        .attr("text-anchor", "middle")
        .attr("font-size", "0.83em")
        .attr("font-weight", "500");

    let xLabel = (totalMinutes > 60) ? "Time (in hours)" : "Time (in minutes)";
    svg.select("text.x-label")
        .text(xLabel)
        .attr("x", (ml_margin.left + ml_width + ml_margin.right) / 2)
        .attr("y", ml_margin.top + ml_height + ml_margin.bottom * 0.75)
        .style("fill", 'black')
        .attr("text-anchor", "middle")
        .attr("font-size", "0.83em")
        .attr("font-weight", "500");

    svg.select("text.y-label")
        .text("Selections")
        .attr("x", ml_margin.left)
        .attr("y", ml_margin.top - 10)
        .style("fill", 'black')
        .attr("text-anchor", "end")
        .attr("font-size", "0.83em")
        .attr("font-weight", "500");
}



function findPathtoHighlight(problem) {

    let chart = d3.select("#multiline-stepchart");

    let mainlines = chart.selectAll('.main_multiline')
        .attr('opacity', 0.6)
        .classed("line-clicked", false);
    mainlines.filter((d, i) => d.id == problem).classed("line-clicked", true)
        .attr('opacity', 1).raise();

}

const insert = (arr, index, newItem) => [
    ...arr.slice(0, index),
    newItem,
    ...arr.slice(index)
];