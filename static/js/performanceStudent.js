colors = [
  "#00E396",
  "#00E396",
  "#ff0000",
  "#ff0000",
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
        name: "Valor",
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
      enabled: true,
    },
    legend: {
      show: false,
    },
    xaxis: {
      categories: ["CANTIDAD APROBADO", " % APROBADO", "CANTIDAD NO APROBADO", "% NO APROBADO", ],
    },
  };

  var chartJudge = new ApexCharts(document.querySelector("#chartJudge"), options);

  chartJudge.render();