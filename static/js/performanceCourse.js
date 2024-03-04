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
  "#50CB93",
  "#FFD369",
];

var options = {
  series: [
    {
      data: values,
    },
  ],
  chart: {
    type: "bar",
    height: 350,
    with: "100%",
  },
  colors: colors,
  plotOptions: {
    bar: {
      borderRadius: 4,
      horizontal: true,
    },
  },
  dataLabels: {
    enabled: true,
  },
  xaxis: {
    categories: labels,
  },
};

var chartStatus = new ApexCharts(
  document.querySelector("#chartStatus"),
  options
);
chartStatus.render();

var options2 = {
  series: [
    {
      data: values2,
    },
  ],
  chart: {
    type: "bar",
    height: 500,
  },
  colors: colors,
  plotOptions: {
    bar: {
      borderRadius: 4,
      horizontal: true,
      offsetY: 60,
      offsetX: 60,
    },
  },
  dataLabels: {
    enabled: true,
  },
  xaxis: {
    categories: labels2,
    labels: {
      style: {
        fontSize: "10px",
      },
      offsetX: 60,
      offsetY: 60
    },
  },
};

var chartPercentage = new ApexCharts(
  document.querySelector("#chartPercentage"),
  options2
);
chartPercentage.render();
