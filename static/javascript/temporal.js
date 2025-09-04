// import Draft from "./auteur/Draft.js";
// import Sequence from "./auteur/Sequence.js";

// for each student, linearize all steps across all problems
// and calculate duration for each step
function processTemporalData(d, problems, problem_type = "all") {
  let allData = [];
  let attemptedProblems = [];

  for (let problem of problems) {
    let problemData = d[problem];

    if (problemData.length === 1) {
      continue;
    }

    if (problem_type === "all" || problemData[0].interface.startsWith(problem_type)) {
      allData = allData.concat(problemData);
      attemptedProblems.push(problem);
    }

  }

  let previousEnd = 0;
  let stepChange = [];

  for (let i = 0; i < allData.length; i++) {
    let step = allData[i];

    /* if (step.action == "start new problem") { */
    //if (step.action.includes("start new problem")) {
    if (step.selection == "") {
      step["duration"] = 0;
      step["start"] = 0;
      step["end"] = 0;
      previousEnd = 0;
    } else {
      let startTime = new Date(step["time"]);

      let lastStep = allData[i-1];
      let lastStepTime = new Date(lastStep["time"]);
      let duration = startTime - lastStepTime;
      step["duration"] = duration;
      step["start"] = previousEnd;
      step["end"] = previousEnd + duration;

      previousEnd = previousEnd + duration;

      if (lastStep.selection !== step.selection
          && lastStep.kc_labels !== step.kc_labels
          && lastStep.action !== "start new problem") {
        stepChange.push(step);
      }
    }
  }

  return [allData, attemptedProblems, stepChange];
}

// render visualization for selected student
function renderStudent(data, problems, problem_type = "all", draft) {
  let colorScheme = {
    "hint": "#ffd68a",
    "incorrect": "#d7191c",
    "correct": "#a6d96a",
    "null": "#bdbdbd"
  };

  let [processed_data, attempted_problems, step_change] = processTemporalData(data, problems, problem_type);

  processed_data = processed_data.map(d => {
    if (d.correctness == "") {
      d.correctness = "NULL";
    }
    d.problemKey = Array.isArray(d.problem) ? d.problem.join(",") : d.problem;
    return d;
  });

  step_change = step_change.map(d => {
    d.problemKey = Array.isArray(d.problem) ? d.problem.join(",") : d.problem;
    return d;
  });

  let svg = d3.select("#temporal");

  let canvas = {
    "height": attempted_problems.length * 30 + 75,
    "width": $("#temporal").parent().width() * 0.95,
    "marginLeft": 110,
    "marginTop": 50,
    "marginRight": 10,
    "marginBottom": 25
  };

  svg.attr("height", canvas.height)
    .attr("width", canvas.width);

  svg.append("g")
    .attr("transform", `translate(${canvas.marginLeft}, ${canvas.marginTop - 35})`)
    .append("text")
    .attr("fill", "#555")
    .attr("font-size", "0.8em")
    .text("ⓘ Hover over bars for more details")
    .append("title")
    .text("Move your mouse over any bar to view details about the step, selection, and input.");

  svg.on('click', function() {
    svg.transition()
      .duration(750)
      .call(zoom.transform, d3.zoomIdentity);
  });

  d3.select("#temporal-clip rect")
    .attr("x", canvas.marginLeft - 10)
    .attr("y", 0)
    .attr("height", canvas.height)
    .attr("width", canvas.width - canvas.marginLeft - canvas.marginRight + 30);

  let yScale = d3.scaleBand()
    .domain(attempted_problems)
    .range([canvas.marginTop, canvas.height - canvas.marginBottom]);

  let xScale = d3.scaleLinear()
    .domain([d3.min(processed_data, d => d["start"]), d3.max(processed_data, d => d["end"])])
    .range([canvas.marginLeft, canvas.width - canvas.marginRight]);

  let tooltip = d3.select("#tooltip")
    .style("position", "fixed")
    .style("visibility", "hidden")
    .style("font-size", "8px")
    .style("border", "solid 1px black")
    .style("border-radius", "2.5px")
    .style("padding", "5px")
    .style("background-color", "white");

  processed_data = processed_data.filter(d => yScale(d.problemKey) != null);
  step_change = step_change.filter(d => yScale(d.problemKey) != null);

  let vis_container = d3.select("#vis-container");

  // Bars
  vis_container.selectAll(".temporalbar")
    .data(processed_data)
    .join("rect")
    .attr("class", "temporalbar")
    .attr("x", d => xScale(d["start"]))
    .attr("width", d => xScale(d['end']) - xScale(d['start']))
    .attr("y", d => yScale(d.problemKey) + 5)
    .attr("height", yScale.bandwidth() - 10)
    .attr("fill", d => colorScheme[d["correctness"].toLowerCase()] || colorScheme["null"])
    .attr("stroke", d => colorScheme[d["correctness"].toLowerCase()] || colorScheme["null"])
    .attr("stroke-width", "0.5px")
    .on("mouseover", function(event, d) {
      toDatabase("hover", "temporal", JSON.stringify(d));
      tooltip.style("visibility", "visible");
    })
    .on("mousemove", function(event, d) {
      let kc = d.kc_labels == "" ? "-" : d.kc_labels.split("'")[1];
      let selection = d.selection;
      let input = d.input;
      tooltip
        .style("left", (event.pageX) + "px")
        .style("top", (event.pageY - 50) + "px")
        .html(
          `<strong>Knowledge Component:</strong> ${kc}<br>
           <strong>Selection:</strong> ${selection}<br>
           <strong>Input:</strong> ${input}`
        );
    })
    .on("mouseout", function() {
      tooltip.style("visibility", "hidden");
    });

  const sequence = new Sequence("correctness", []);
  draft.layer("#temporal").select(".temporalbar").augment(sequence.getAugs());

  // Start points
  let start_only = processed_data.filter(d => d.action == "start new problem");

  d3.select("#start-points")
    .selectAll(".start")
    .data(start_only)
    .join("circle")
    .attr("class", "start")
    .attr("cx", d => xScale(d["start"]))
    .attr("cy", d => yScale(d.problemKey) + yScale.bandwidth() / 2)
    .attr("r", 5)
    .attr("fill", "none")
    .attr("stroke", "black")
    .attr("stroke-width", "1.5px");

  // Completion stars
  let complete_only = processed_data.filter(d => d.selection == "done" && d.correctness == "CORRECT");

  d3.select("#complete-points")
    .selectAll(".complete")
    .data(complete_only)
    .join("text")
    .attr("class", "complete")
    .attr("x", d => xScale(d["end"]) + 10)
    .attr("y", d => yScale(d.problemKey) + yScale.bandwidth() / 2 + 6)
    .attr("fill", "black")
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .attr("alignment-baseline", "middle")
    .text("*");

  // Step change lines
  d3.select("#step-change")
    .selectAll(".change")
    .data(step_change)
    .join("line")
    .attr("class", "change")
    .attr("x1", d => xScale(d["start"]))
    .attr("x2", d => xScale(d["start"]))
    .attr("y1", d => yScale(d.problemKey) + 4.5)
    .attr("y2", d => yScale(d.problemKey) + yScale.bandwidth() - 4.5)
    .attr("fill", "none")
    .attr("stroke", "black")
    .attr("stroke-width", "1.5px");

  let gy = svg.select('#y-axis');
  let yAxis = d3.axisLeft(yScale).tickSize(3).ticks(5).tickPadding([10]);

  gy.attr('transform', `translate(${canvas.marginLeft}, 0)`)
    .call(yAxis.tickFormat(d => {
      let text = (d ?? "").toString();
      return text.length > 20 ? text.slice(0, 20) + "..." : text;
    }))
    .selectAll(".tick text")
    .append("title")
    .text(d => (d ?? "").toString());

  // X-axis
  function formatTime(t) {
    let seconds = t / 1000;
    if (seconds >= 86400) {
      let days = Math.floor(seconds / 86400);
      let hours = Math.floor(seconds % 86400 / 3600);
      return `${days}days ${hours}h`;
    } else if (seconds >= 3600) {
      let hours = Math.floor(seconds / 3600);
      let minutes = Math.floor(seconds % 3600 / 60);
      return `${hours}h ${minutes}mins`;
    } else if (seconds >= 60) {
      let minutes = Math.floor(seconds / 60);
      let r = seconds % 60;
      return `${minutes}mins ${r}s`;
    } else {
      return `${seconds}s`;
    }
  }

  let gx = svg.select('#x-axis');
  let xAxis = d3.axisBottom(xScale).tickSize(3).ticks(5).tickFormat(formatTime);

  gx.attr('transform', `translate(0, ${canvas.height - canvas.marginBottom})`)
    .call(xAxis);
}



function update_sequence_selectors(draft) {
  let opt = [{"desc":"show when students make three consecutive correct steps", "value":"correct", "seq": ["CORRECT", "CORRECT", "CORRECT"]},
             {"desc":"show when students make a correct step after asking for a hint", "value":"hintcorrect", "seq": ["HINT", "CORRECT"]},
             {"desc":"show when students make an incorrect step after asking for a hint", "value":"hintincorrect", "seq": ["HINT", "INCORRECT"]},
             {"desc":"show when students make three consecutive incorrect steps", "value":"incorrect", "seq": ["INCORRECT", "INCORRECT", "INCORRECT"]},
             {"desc":"show all", "value":"all", "seq": []}]

  if (document.querySelector('#temporalSelectors *') === null) {
    let select = document.getElementById('temporalSelectors');

    for (let pt of opt) {
      optionContainer = document.createElement("div");

      var checkbox = document.createElement('input');
      checkbox.type = "radio";
      checkbox.value = pt.value;
      checkbox.id = pt.value;
      if (pt.value == "all") {checkbox.checked = true}

      checkbox.addEventListener(
         'change',
         function() { 
            let allOptions = document.querySelectorAll('#temporalSelectors input');

            for (let allOpt of allOptions) {
              if (allOpt.id === pt.value) {
                continue
              } else {
                allOpt.checked = false;
              }
            }

            const sequence = new Sequence("correctness", pt.seq);
            draft.select(".temporalbar").augment(sequence.getAugs());

         },
         false
      );
      checkbox.style.marginRight = "10px";

      var label = document.createElement('label')
      label.appendChild(document.createTextNode(pt.desc));

      optionContainer.appendChild(checkbox);
      optionContainer.appendChild(label);

      select.appendChild(optionContainer);
    }
  } else {
    // clear current dropdown values in select
    let inputs = document.querySelectorAll('#temporalSelectors input');
    for (let option of inputs) {
      option.remove();
    }

    let lables = document.querySelectorAll('#temporalSelectors label');
    for (let option of lables) {
      option.remove();
    }

    let select = document.getElementById('temporalSelectors');

    for (let pt of opt) {
      optionContainer = document.createElement("div");

      var checkbox = document.createElement('input');
      checkbox.type = "radio";
      checkbox.value = pt.value;
      checkbox.id = pt.value;
      if (pt.value == "all") {checkbox.checked = true}

      checkbox.addEventListener(
         'change',
         function() { 
            let allOptions = document.querySelectorAll('#temporalSelectors input');

            for (let allOpt of allOptions) {
              if (allOpt.id === pt.value) {
                continue
              } else {
                allOpt.checked = false;
              }
            }

            const sequence = new Sequence("correctness", pt.seq);
            draft.augment(sequence.getAugs());
         },
         false
      );
      checkbox.style.marginRight = "10px";

      var label = document.createElement('label')
      label.appendChild(document.createTextNode(pt.desc));

      optionContainer.appendChild(checkbox);
      optionContainer.appendChild(label);

      select.appendChild(optionContainer);
    }
  }
}

// process data and render based on whether student or problem is selected
function renderTemporal(data, id, problem_type, view_by="student"){

  let draft = new Draft();

  draft.exclude({"name": ["fill"]});

  processed_data = data[id];

  update_sequence_selectors(draft);
  renderStudent(processed_data, Object.keys(processed_data), problem_type, draft);
         
}