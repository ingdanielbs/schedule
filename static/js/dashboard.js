colors = ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0', '#3F51B5', '#546E7A', '#D4526E', '#8D5B4C', '#F86624', '#D7263D', '#1B998B', '#2E294E', '#F46036', '#E2C044']
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
    series: [{
    data: values2
  }],
    chart: {
    type: 'bar',
    height: 350
  },
  colors: colors,
  plotOptions: {
    bar: {
      borderRadius: 4,
      horizontal: true,
    }
  },
  dataLabels: {
    enabled: false
  },
  xaxis: {
    categories: labels2,
  }
  };

  var chartStudent = new ApexCharts(document.querySelector("#chartStudent"), options2);
  chartStudent.render();