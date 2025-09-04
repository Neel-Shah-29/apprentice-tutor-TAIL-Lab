const overviewGroups = ['Question Type', 'Correct', 'Incorrect', 'Skipped'];
let groupsShown = ['problemType', 'numCorrect', 'numIncorrect']; //default
// const ov_barsColorScale = d3.scaleOrdinal()
//     .range(['#4DD16C', '#D14D4D', '#DADADA']);

const ov_barsColorScale = {"numCorrect":'#4DD16C', "numIncorrect":'#D14D4D', "skipped":'#DADADA'};

function renderOverviewVis(d, groupsShown = ['problemType', 'numCorrect', 'numIncorrect']) {

    let problemTypes = Object.keys(d);
    let overviewData = [];
    for (let p of problemTypes) {
        let students = Object.keys(d[p]);
        let numCorrect = 0;
        let numIncorrect = 0;
        let skipped = 0;
        // let numNotStarted = 0; students who haven't attempted this question?
        for (let student of students) {
            let questions = Object.keys(d[p][student]);
            for (let question of questions) {

                let numSteps = d[p][student][question].length;
                if (d[p][student][question][numSteps - 1].correctness === 'CORRECT' && d[p][student][question][numSteps - 1].selection === "done") {
                    numCorrect++;
                } else if (numSteps <= 1) { // started but didn't attempt any questions
                    skipped++;
                } else {
                    numIncorrect++;
                } 
            }
        }
        overviewData.push({
            problemType: p,
            numCorrect: numCorrect,
            numIncorrect: numIncorrect,
            skipped: skipped
        });
    }
    overviewData.columns = ['problemType', 'numCorrect', 'numIncorrect', 'skipped'];
    // ov_barsColorScale.domain(overviewData.columns.slice(1)); // set domain of color scale

    let curOvData = [];
    for (let probType of overviewData) {
        let entry = {};
        for (let p of Object.keys(probType)) {
            if (groupsShown.includes(p))
                entry[p] = probType[p];
        }
        curOvData.push(entry);
    }
    curOvData.columns = [groupsShown[0]].concat(groupsShown.slice(1).sort());
    renderStackedBarChart(curOvData, overviewData, groupsShown);
}

function renderStackedBarChart(curOvData, overviewData, groupsShown) {
    const vis_margin = { top: 30, right: 80, bottom: 50, left: 135 };
    const parent = document.getElementById("overview-vis").parentElement.getBoundingClientRect(); //$("#overview-vis").parent()
    const vis_width = parent.width * 0.95 - vis_margin.left - vis_margin.right,
        vis_height = 250 - vis_margin.top - vis_margin.bottom;

    const svg = d3.select("#overview-vis")
        .attr("width", vis_width + vis_margin.left + vis_margin.right)
        .attr("height", vis_height + vis_margin.top + vis_margin.bottom);

    const chart = svg.select('g.elements')
        .attr("transform", `translate(${vis_margin.left},${vis_margin.top})`);

    const questions = chart.select('.questions');
    let stackedData = d3.stack().keys(curOvData.columns.slice(1))(curOvData);
    // Add Y axis
    let y = d3.scaleBand()
        .domain(curOvData.map(d => d.problemType).sort()) // List of groups = value of the first column
        .range([vis_height, 0])
        .padding([0.2]);

    // Add X axis
    let problemsTypes = Object.keys(curOvData);
    let maxQuestionsSeen = 0;
    let fields = [...groupsShown];
    fields.splice(0, 1);

    for (let problem of problemsTypes) {
        let p = curOvData[problem];
        let s = 0;
        for (let grp of fields) {
            s = p[grp] ? s + p[grp] : s;
        }
        if (s > maxQuestionsSeen)
            maxQuestionsSeen = s;
    }

    //const x = d3.scaleLinear()
    let x = d3.scaleLinear()
        .domain([0, maxQuestionsSeen]) // max number of questions solved/attempted
        .range([0, vis_width]);

    let xAxis = d3.axisBottom(x);
    let xAxisG = chart.select(".x-axis")
        .attr("transform", `translate(0, ${vis_height})`)
        .call(xAxis);

    chart.select(".y-axis")
        .call(d3.axisLeft(y).tickSizeOuter(0))
        .selectAll("text")
        .attr("class", "bar-labels");

    d3.select('#overviewvis-clip rect')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', vis_width)
        .attr('height', vis_height);

    stackedData = stackedData.map((stack, i) => stack.map(substack => {substack.key = stack.key; return substack}))

    stackedData = [].concat.apply([], stackedData);

    var stackedGroups = questions.selectAll(".bar")
        .data(stackedData)
        .join("rect")
        .attr("class", d => "bar")
        .attr("x", d => x(d[0]))
        .attr("y", d => y(d.data.problemType))
        .attr("height", y.bandwidth())
        .attr("width", d => x(d[1]) - x(d[0]))
        .attr("fill", d => ov_barsColorScale[d.key])
        .attr("stroke", "black")
        .attr("stroke-width", 0)
        .attr('clip-path', 'url(#overviewvis-clip)')
        .on("mouseover", function(d, i) {
          toDatabase("hover", "overview", i.data.problemType) });

    // labels
    svg.select("text.x-label")
        .text("Number of questions")
        .attr("x", (vis_margin.left + vis_width + vis_margin.right) / 2)
        .attr("y", vis_margin.top + vis_height + vis_margin.bottom * 0.6)
        .attr("dx", 0)
        .style("fill", 'black')
        .attr("text-anchor", "middle")
        .attr("font-size", "0.8em")
        .attr("font-weight", "500");

    svg.select("text.y-label")
        .text("Question Type")
        .attr("x", vis_margin.left)
        .attr("y", vis_margin.top - 10)
        // .attr("transform", "rotate(-90)")
        .style("fill", 'black')
        .attr("text-anchor", "end")
        .attr("font-size", "0.8em")
        .attr("font-weight", "500");

    // legend
    svg.selectAll(".legendrect")
        .data(overviewData.columns.slice(1))
        .join("rect")
        .attr("id", (d, i) => `rect-${i}`)
        .attr("class", "legendrect")
        .attr("x", vis_margin.left + vis_width + 10)
        .attr("y", (d, i) => vis_margin.top + 15 * i)
        .attr("height", 10)
        .attr("width", 10)
        .attr("stroke", d => ov_barsColorScale[d])
        .attr("stroke-width", 2)
        .attr("fill", d => groupsShown.includes(d) ? ov_barsColorScale[d] : "white")
        .style("cursor", "pointer")
        .on("mousedown", function (d, i) {
            toDatabase("select", "overview_legend", i);
            handleLegendClick(d, i, overviewData);
        });

    svg.selectAll(".legendtext")
        .data(overviewGroups.slice(1))
        .join("text")
        .attr("class", "legendtext")
        .attr("x", vis_margin.left + vis_width + 25)
        .attr("y", (d, i) => vis_margin.top + 15 * i + 7)
        .text(d => d)
        .attr("alignment-baseline", "middle")
        .attr("font-size", 8)
        .style("cursor", "pointer")
        .on("mousedown", function (d, i) {
            toDatabase("select", "overview_legend", i);
            handleLegendClick(d, i, overviewData);
        });

    // set clickable area inside chart to deselect lines
    let zoomableArea = chart.select('rect')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', vis_width)
        .attr('height', vis_height)
        .attr('fill', 'transparent')
        .attr('pointer-events', 'visible');

    function overViewZoom() {
        let t = d3.event.transform;
        /* let k = t.k / vis_z.k;
        vis_z = t; */
        // update x axis
        let newXScale = t.rescaleX(x);
        //d3.select('#overview-vis .x-axis').call(xAxis.scale(newXScale));

        /* x.range([0, vis_width].map(d => t.applyX(d)));
        svg.select(".x-axis").call(xAxis); */
        xAxisG.call(xAxis.scale(newXScale));

        // update stack chart
        stackedGroups.selectAll("rect")
            // enter a second time = loop subgroup per subgroup to add all rectangles
            .data(d => d)
            .join("rect")
            .attr("class", d => { return d.data.problemType })
            //.attr("x", d => x(d[0])* t.k) //** nice
            //.attr("x", d => { if (k === 1) return t.x + x(d[0])* t.k; else return x(d[0])* t.k; }) //** nice
            //.attr("x", d => t.x + x(d[0])* t.k)
            //.attr("x", d => x(d[0])* t.k) //** nice
            .attr("x", d => newXScale(d[0]))
            .attr("y", d => y(d.data.problemType))
            .attr("height", y.bandwidth())
            //.attr("width", d => newXScale(d[1]) - newXScale(d[0]))
            .attr("width", d => x(d[1]) * t.k - x(d[0]) * t.k) //** width increase */
            //.attr("width", d => newXScale(d[1]) - newXScale(d[0])) //** width increase */
            .attr("stroke", "black")
            .attr("stroke-width", 0);

    }

    let extent = [[0, 0], [vis_width, vis_height]];
    let chartZoom = d3.zoom()
        .translateExtent(extent)
        .extent(extent)
        .scaleExtent([1, 10000])
        .on('zoom', overViewZoom);

    zoomableArea.call(chartZoom);
}

function handleLegendClick(d, i, overviewData) {
    let label = i;
    if (groupsShown.includes(label)) { // is currently shown 
        d3.select(`#rect-${i}`).attr("fill", "white");
        // remove from shown grps list
        let j = groupsShown.indexOf(label);
        if (j > -1) {
            groupsShown.splice(j, 1);
        }
    } else {
        d3.select(`#rect-${i}`).attr("fill", d => ov_barsColorScale[label]);
        groupsShown.push(label);
    }
    // if skipped is present, move it end of list to show it at the end of the stacked bar chart
    /* if (groupsShown.includes('numIncorrect')) {
        let j = groupsShown.indexOf('numIncorrect');
        groupsShown.push(groupsShown.splice(j, 1)[0]);
    } */
    if (groupsShown.includes('skipped')) {
        let j = groupsShown.indexOf('skipped');
        groupsShown.push(groupsShown.splice(j, 1)[0]);
    }
    renderOverviewVis(processedData[0], groupsShown);
}