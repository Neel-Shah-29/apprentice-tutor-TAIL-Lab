// given a data set of all steps performed by all students
// group the data by problem and by student
function processData(data) {
  let data_by_interface = {};

  for (let d of data) {
    let problem_interface = d["interface"].endsWith(".html") ? d["interface"].slice(0, -5) : d["interface"];
    let start_state = d["start_state"].replaceAll("'", '"');
    let problem_content = JSON.parse(start_state)["initial_problem"];
    let student = d["userid"];

    // if interface has not been seen yet, create new dictionary key
    if (!(problem_interface in data_by_interface)) {
      data_by_interface[problem_interface] = {};
    }

    let users = data_by_interface[problem_interface];

    // if problem has not been seen yet, create new dictionary key
    if (!(student in users)) {
      data_by_interface[problem_interface][student] = {};
    }

    let problem_attempts = data_by_interface[problem_interface][student];

    // if student has not attempted problem
    // add student to the problem in the dictionary
    if (!(problem_content in problem_attempts)) {
      problem_attempts[problem_content] = [];
    }

    problem_attempts[problem_content].push(d);
  }

  let data_by_student = {};
  let regex_by_student = {};

  let students = new Set();

  for (let d of data) {
    let start_state = d["start_state"].replaceAll("'", '"');
    let problem_content = JSON.parse(start_state)["initial_problem"];

    // This line converts each step into a string for quick regex search
    // For now, this is only a simple record of correctness
    // Can be extended to include more information, such as timing data
    let problem_regex = d["action"] == "start new problem" ? "Snp" : d["correctness"][0];

    let student = d["userid"];

    // if student has not been seen yet, create new dictionary key
    if (!(student in data_by_student)) {
      data_by_student[student] = {};
      regex_by_student[student] = '';
    }

    regex_by_student[student] = regex_by_student[student] + problem_regex;

    let student_data = data_by_student[student];

    // if new problem is attempted by student
    // add problem to the student in the dictionary
    if (!(problem_content in student_data)) {
      student_data[problem_content] = [];
    }

    d['problem'] = problem_content;

    student_data[problem_content].push(d);
  }

  for (let pt of Object.keys(data_by_interface)) {
    let pt_students = data_by_interface[pt];
    for (let student of Object.keys(pt_students)) {
      let student_problems = pt_students[student];      
      for (let problem of Object.keys(student_problems)) {
        if (student_problems[problem].length <= 1) {
          delete student_problems[problem];
        }
      }
      if (Object.keys(pt_students[student]).length <= 0) {
        delete pt_students[student];
      }
    }
    if (Object.keys(data_by_interface[pt]).length <= 0) {
      delete data_by_interface[pt];
    }
  }

  for (let student of Object.keys(data_by_student)) {
    let student_problems = data_by_student[student];
    for (let problem of Object.keys(student_problems)) {
      if (student_problems[problem].length <= 1) {
        delete student_problems[problem]
      }
    }
    if (Object.keys(data_by_student[student]).length <= 0) {
      delete data_by_student[student]
    }
  }

  return [data_by_interface, data_by_student, regex_by_student]
}

// get labels for each interface
function getLabels(data) {
  let interfaceLabels = new Map();
  for (let d of data) {
    if (d.kc_labels && d.kc_labels != '') {
      let l = d.kc_labels.replaceAll("'", '"');
      let label = JSON.parse(l);
      let problem_interface = d["interface"].endsWith(".html") ? d["interface"].slice(0, -5) : d["interface"];

      if (interfaceLabels.has(problem_interface)) {
        let labels = interfaceLabels.get(problem_interface);
        //if (label.length !== 0 && !labels[0].includes(label[0]))
        labels.push([label[0], d.selection]);
      } else {
        if (label.length >= 0)
          interfaceLabels.set(problem_interface, [[label[0], d.selection]]);
        else interfaceLabels.set(problem_interface, []);
      }
    }
  }
}

// hard-coded values for area box method
// function getAreaBoxLabels() {
//   /**
//    * lists beginning with s are static groups, 
//    * lists beginning with d are dynamic groups indicating that this group may grow
//    * */
//   return [
//     ['s', 'a_value', 'b_value', 'c_value'],
//     ['s', 'product_ac'],
//     ['d', 'factor_1_ac_1', 'factor_2_ac_1', 'sum_factor_1', 'sum_b_1',
//       'factor_1_ac_2', 'factor_2_ac_2', 'sum_factor_2', 'sum_b_2',
//       'factor_1_ac_3', 'factor_2_ac_3', 'sum_factor_3', 'sum_b_3'],
//     ['s', 'sx_value', 't_value', 'qx_value', 'ax2_value', 'mx_value', 'r_value', 'nx_value', 'c_table_value'],
//     ['s', 'first_expression', 'second_expression'],
//     ['s', 'final_answer'],
//     ['s', 'done'] // done - buttom click
//   ];
// }

// function getGroupedLabels(height, groupedLabels, numLabels, labelHt, numPadding) {
//   const paddingHt = (height - (labelHt * numLabels)) / numPadding;
//   let posY = labelHt;
//   let labelPosY = {};
//   groupedLabels.forEach(function (group) {
//       group.forEach(function (label, i) {
//           if (i !== 0) {
//               labelPosY[label] = posY;
//               posY = posY + labelHt;
//           }
//       });
//       posY = posY + paddingHt;
//   });
//   return labelPosY;
// }

function toDatabase(interaction, source, input) {
  
  var current_url = window.location.href;

  $.ajax({
    type: "POST",
    url: "/vis_transaction",
    data: JSON.stringify({
            "user":"user1",
            "student":selectedStudent,
            "problemType":selectedProblemType,
            "problem": selectedProblem ? selectedProblem : "none",
            "interaction": interaction,
            "source": source,
            "input": input,
            "current_url": current_url
        }),
    success: function(result) {
            // console.log(result)
        },
    error: function(result) {
            console.log(result);
        },
    dataType: "json",
    contentType: "application/json"
});
}

function formatAxisWithTooltip(axis, maxLen = 20) {
  return function(selection) {
    selection.call(
      axis.tickFormat(d => {
        let text = (d ?? "").toString();
        return text.length > maxLen ? text.slice(0, maxLen) + "..." : text;
      })
    );
    selection.selectAll(".tick text")
      .append("title")
      .text(d => (d ?? "").toString());
  };
}


