var options = {
    chart: {
      type: "bar",
    },
    series: [
      {
        name: "Porcentaje",
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