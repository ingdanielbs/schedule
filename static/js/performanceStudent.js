colors = [
  "#00E396",
  "#ff0000",
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
  "#50CB93",
  "#FFD369",
];


var options = {
    chart: {
      type: "bar",
      height: 300,
    },
    series: [
      {
        name: "Porcentaje",
        data: values
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
      categories: ["APROBADO", "NO APROBADO"],
    },
  };

  var chartJudge = new ApexCharts(document.querySelector("#chartJudge"), options);

  chartJudge.render();