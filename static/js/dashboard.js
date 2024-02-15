colors = [
  "#008FFB",
  "#00E396",
  "#FEB019",
  "#FF4560",
  "#775DD0",
  "#3F51B5",
  "#546E7A",
  "#D4526E",
  "#8D5B4C",
  "#F86624",
  "#D7263D",
  "#1B998B",
  "#2E294E",
  "#F46036",
  "#E2C044",
];
var options = {
  chart: {
    type: "bar",
  },
  series: [
    {
      name: "Instructor",
      data: values,
    },
  ],
  colors: colors,
  plotOptions: {
    bar: {
      columnWidth: "45%",
      distributed: true,
    },
  },
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: false,
  },
  xaxis: {
    categories: labels,
  },
};

var chart = new ApexCharts(document.querySelector("#chart"), options);

chart.render();

var options2 = {
  series: [
    {
      data: values2,
    },
  ],
  chart: {
    type: "bar",
    height: 350,
  },
  colors: colors,
  plotOptions: {
    bar: {
      borderRadius: 4,
      horizontal: true,
    },
  },
  dataLabels: {
    enabled: false,
  },
  xaxis: {
    categories: labels2,
  },
};

var chartStudent = new ApexCharts(
  document.querySelector("#chartStudent"),
  options2
);
chartStudent.render();

var options3 = {
  series: values3,
  chart: {
    type: "donut",
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: 200,
        },
        legend: {
          position: "bottom",
          show: true,
        },
      },
    },
  ],
  labels: labels3,
  colors: ["#008FFB", "#fa89ce"],
};

var chartGender = new ApexCharts(
  document.querySelector("#chartGender"),
  options3
);
chartGender.render();


var options4 = {
  chart: {
    type: "bar",
  },
  series: [
    {
      name: "Aprendices",
      data: values4,
    },
  ],
  colors: colors,
  plotOptions: {
    bar: {
      columnWidth: "45%",
      distributed: true,
    },
  },
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: false,
  },
  xaxis: {
    categories: labels4,
  },
};

var chartProgram = new ApexCharts(document.querySelector("#chartProgram"), options4);

chartProgram.render();

var options5 = {
  series: [
    {
      data: values5,
    },
  ],
  chart: {
    type: "bar",
    height: 350,
  },
  colors: colors,
  plotOptions: {
    bar: {
      borderRadius: 4,
      horizontal: true,
    },
  },
  dataLabels: {
    enabled: false,
  },
  xaxis: {
    categories: labels5,
  },
};

var chartCourses = new ApexCharts(document.querySelector("#chartCourses"), options5);

chartCourses.render();