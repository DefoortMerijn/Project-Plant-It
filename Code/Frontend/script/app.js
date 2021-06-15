'use strict';
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
let htmlData, htmlHome, htmlOverview, htmlTemplive, htmlMoisturelive, htmlLDRlive, htmlLdrLog, htmlMoistureLog, htmlTempLog, htmlIrrigation, htmlPlantWater, htmlPlantTimer, htmlTimer;
let currentID;
let charttemp;
let chartldr;
let chartmoist;

const callbackWater = function (data) {
  console.log(data);
  console.log(lanIP);
  socket.emit('F2B_send_water', data);
};
const callbacktimer = function () {
  console.log('ADD antw van server');
  console.log('Add gelukt');
  htmlTimer = htmlPlantTimer.options[htmlPlantTimer.selectedIndex].innerText;
  document.getElementById('name').value = '';
  document.querySelector('.js-timer-time').value = '';
  document.querySelector('.js-timer-day').value = '';
  htmlPlantTimer.selectedIndex = 0;
};
//#region ***  Event Listeners - listenTo___            ***********
const listenToSocket = function () {
  socket.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
  socket.on('B2F_new_data', function (jsonObject) {
    console.log(jsonObject.data);
    if (htmlOverview) {
      getUpdatedDataTemp();
      getUpdatedDataMoisture();
      getUpdatedDataLdr();
    }
    if (htmlLdrLog) {
      getLdrLog();
    }
    if (htmlMoistureLog) {
      getMoistureLog();
    }
    if (htmlTempLog) {
      getTempLog();
    }
  });
};
const listenToClickBtnWater = function () {
  const btn = document.querySelector('.js-addwater-button');
  btn.addEventListener('click', function () {
    console.log('add water');
    const plant = htmlPlantWater.value;
    console.log(plant);
    handleData(`http://${lanIP}/api/v1/Water/${plant}`, callbackWater, null, 'GET');
  });
};

const listenToClickBtnTimer = function () {
  const btn = document.querySelector('.js-timer-button');
  btn.addEventListener('click', function () {
    console.log('Toevoegen Timer');

    const jsonObject = {
      Name: document.querySelector('.js-timer-name').value,
      Time: document.querySelector('.js-timer-time').value + ':00',
      Day: document.querySelector('.js-timer-day').value,
      Plant: htmlPlantTimer.value,
    };
    console.log(jsonObject);
    handleData(`http://${lanIP}/api/v1/Timer`, callbacktimer, null, 'POST', JSON.stringify(jsonObject));
  });
};
//Chart Temperature
const showDataTemp = function (temp) {
  console.log('draw feed temp');
  console.log(temp);
  let converted_data = [];
  converted_data.push(temp['Value']);

  drawChartTemp(converted_data);
};
const drawChartTemp = function (data) {
  console.log(data);
  var options = {
    chart: {
      type: 'radialBar',
    },

    series: [data],
    plotOptions: {
      radialBar: {
        hollow: {
          margin: 0,
          size: '70%',
          background: '#293450',
        },
        track: {
          dropShadow: {
            enabled: true,
            top: 2,
            left: 0,
            blur: 4,
            opacity: 0.15,
          },
        },

        dataLabels: {
          showOn: 'always',
          name: {
            offsetY: -10,
            show: true,
            color: '#f5f5f5',
            fontSize: '16px',
          },
          value: {
            formatter: function (val) {
              return parseInt(val) + '°C';
            },
            color: '#57d131',
            fontSize: '30px',
            fontWeight: 'bold',
            show: true,
          },
        },
      },
    },

    fill: {
      colors: ['#57d131'],
    },

    stroke: {
      lineCap: 'round',
    },
    labels: ['Temperature'],
    noData: {
      text: 'Loading...',
    },
  };
  charttemp = new ApexCharts(document.querySelector('.js-charttemp'), options);
  charttemp.render();
};

const showUpdatedDataTemp = function (temp) {
  console.log('update feed temp');
  console.log(temp);
  let converted_data = [];
  converted_data.push(temp['Value']);
  updateChartTemp(converted_data);
};

const updateChartTemp = function (data) {
  console.log('updating');
  console.log(data);
  charttemp.updateOptions({
    chart: {
      type: 'radialBar',
    },

    series: [data],
    plotOptions: {
      radialBar: {
        hollow: {
          margin: 0,
          size: '70%',
          background: '#293450',
        },
        track: {
          dropShadow: {
            enabled: true,
            top: 2,
            left: 0,
            blur: 4,
            opacity: 0.15,
          },
        },

        dataLabels: {
          showOn: 'always',
          name: {
            offsetY: -10,
            show: true,
            color: '#f5f5f5',
            fontSize: '16px',
          },
          value: {
            formatter: function (val) {
              return parseInt(val) + '°C';
            },
            color: '#57d131',
            fontSize: '30px',
            fontWeight: 'bold',
            show: true,
          },
        },
      },
    },

    fill: {
      colors: ['#57d131'],
    },

    stroke: {
      lineCap: 'round',
    },
    labels: ['Temperature'],
    noData: {
      text: 'Loading...',
    },
  });
};

// Chart LDR
('');
const showDataLdr = function (ldr) {
  console.log('draw feed ldr');
  console.log(ldr);
  let converted_data = [];
  converted_data.push(ldr['Value']);
  drawChartLdr(converted_data);
};

const showUpdatedDataLdr = function (ldr) {
  console.log('update feed ldr');
  console.log(ldr);
  let converted_data = [];
  converted_data.push(ldr['Value']);
  updateChartLdr(converted_data);
};

const updateChartLdr = function (data) {
  console.log('update feed LDR');
  chartldr.updateOptions({
    chart: {
      type: 'radialBar',
    },

    series: [data],

    plotOptions: {
      radialBar: {
        hollow: {
          margin: 0,
          size: '70%',
          background: '#293450',
        },
        track: {
          dropShadow: {
            enabled: true,
            top: 2,
            left: 0,
            blur: 4,
            opacity: 0.15,
          },
        },

        dataLabels: {
          showOn: 'always',
          name: {
            offsetY: -10,
            show: true,
            color: '#f5f5f5',
            fontSize: '16px',
          },
          value: {
            color: '#57d131',
            fontSize: '30px',
            fontWeight: 'bold',
            show: true,
          },
        },
      },
    },
    fill: {
      colors: ['#57d131'],
    },

    stroke: {
      lineCap: 'round',
    },
    labels: ['Light Intesnity'],
  });
};

const drawChartLdr = function (data) {
  var options = {
    chart: {
      type: 'radialBar',
    },

    series: [data],

    plotOptions: {
      radialBar: {
        hollow: {
          margin: 0,
          size: '70%',
          background: '#293450',
        },
        track: {
          dropShadow: {
            enabled: true,
            top: 2,
            left: 0,
            blur: 4,
            opacity: 0.15,
          },
        },

        dataLabels: {
          showOn: 'always',
          name: {
            offsetY: -10,
            show: true,
            color: '#f5f5f5',
            fontSize: '16px',
          },
          value: {
            color: '#57d131',
            fontSize: '30px',
            fontWeight: 'bold',
            show: true,
          },
        },
      },
    },
    fill: {
      colors: ['#57d131'],
    },

    stroke: {
      lineCap: 'round',
    },
    labels: ['Light Intesnity'],
  };
  chartldr = new ApexCharts(document.querySelector('.js-chartldr'), options);
  chartldr.render();
};

//Chart Moisture

const showDataMoisture = function (moist) {
  console.log('draw feed moist');
  console.log(moist);
  let converted_data = [];
  converted_data.push(moist['Value']);
  drawChartMoisture(converted_data);
};
const showUpdatedDataMoisture = function (moist) {
  console.log('update feed Moisture');
  console.log(moist);
  let converted_data = [];
  converted_data.push(moist['Value']);
  updateChartMoisture(converted_data);
};
const updateChartMoisture = function (data) {
  console.log('update feed Moisture');
  console.log(data);
  chartmoist.updateOptions({
    chart: {
      type: 'radialBar',
    },

    series: [data],

    plotOptions: {
      radialBar: {
        hollow: {
          margin: 0,
          size: '70%',
          background: '#293450',
        },
        track: {
          dropShadow: {
            enabled: true,
            top: 2,
            left: 0,
            blur: 4,
            opacity: 0.15,
          },
        },

        dataLabels: {
          showOn: 'always',
          name: {
            offsetY: -10,
            show: true,
            color: '#f5f5f5',
            fontSize: '16px',
          },
          value: {
            color: '#57d131',
            fontSize: '30px',
            fontWeight: 'bold',
            show: true,
          },
        },
      },
    },
    fill: {
      colors: ['#57d131'],
    },

    stroke: {
      lineCap: 'round',
    },
    labels: ['Moisture Level'],
  });
};
const drawChartMoisture = function (data) {
  console.log('draw');
  var options = {
    chart: {
      type: 'radialBar',
    },

    series: [data],

    plotOptions: {
      radialBar: {
        hollow: {
          margin: 0,
          size: '70%',
          background: '#293450',
        },
        track: {
          dropShadow: {
            enabled: true,
            top: 2,
            left: 0,
            blur: 4,
            opacity: 0.15,
          },
        },

        dataLabels: {
          showOn: 'always',
          name: {
            offsetY: -10,
            show: true,
            color: '#f5f5f5',
            fontSize: '16px',
          },
          value: {
            color: '#57d131',
            fontSize: '30px',
            fontWeight: 'bold',
            show: true,
          },
        },
      },
    },
    fill: {
      colors: ['#57d131'],
    },

    stroke: {
      lineCap: 'round',
    },
    labels: ['Moisture Level'],
  };
  chartmoist = new ApexCharts(document.querySelector('.js-chartmoist'), options);
  chartmoist.render();
};

// LOGS
const showLogMoisture = function (data) {
  console.log(data);

  let converted_labels = [];
  let converted_data = [];
  for (const moist of data) {
    converted_data.push(moist['Value']);
    converted_labels.push(moist['Date']);
  }
  drawLogMoisture(converted_labels, converted_data);
};
const drawLogMoisture = function (labels, data) {
  var options = {
    chart: {
      background: ['#F5F5F5'],
      type: 'line',
    },
    stroke: {
      curve: 'smooth',
    },
    dataLabels: {
      enabled: false,
    },
    series: [{ name: 'Moisture Level', data: data }],
    colors: ['#57d131'],
    labels: labels,

    noData: {
      text: 'There is no data to be found :(',
    },
  };

  var chart = new ApexCharts(document.querySelector('.js-moistureLog'), options);
  chart.render();
};

const showLogLdr = function (data) {
  console.log(data);

  let converted_labels = [];
  let converted_data = [];
  for (const ldr of data) {
    converted_data.push(ldr['Value']);
    converted_labels.push(ldr['Date']);
  }
  drawLogLdr(converted_labels, converted_data);
};
const drawLogLdr = function (labels, data) {
  var options = {
    chart: {
      type: 'line',
      background: ['#F5F5F5'],
    },
    stroke: {
      curve: 'smooth',
    },
    dataLabels: {
      enabled: false,
    },
    series: [{ name: 'Light Intensity', data: data }],

    colors: ['#57d131'],

    labels: labels,
    noData: {
      text: 'There is no data to be found :(',
    },
  };

  var chart = new ApexCharts(document.querySelector('.js-ldrLog'), options);
  chart.render();
};

const showLogTemp = function (data) {
  console.log(data);

  let converted_labels = [];
  let converted_data = [];
  for (const temp of data) {
    converted_data.push(temp['Value']);
    converted_labels.push(temp['Date']);
  }
  drawLogTemp(converted_labels, converted_data);
};
const drawLogTemp = function (labels, data) {
  var options = {
    chart: {
      type: 'line',
      background: ['#F5F5F5'],
    },
    stroke: {
      curve: 'smooth',
    },
    dataLabels: {
      enabled: false,
    },
    series: [{ name: 'Temperature(°C)', data: data }],
    colors: ['#57d131'],
    labels: labels,
    noData: {
      text: 'There is no data to be found :(',
    },
  };

  var chart = new ApexCharts(document.querySelector('.js-tempLog'), options);
  chart.render();
};

const showSelectPlant = function (data) {
  console.log(data);
  let html = '<option value="" selected disabled>Choose Plant</option>';
  for (const plant of data) {
    html += `
    <option value="${plant.Id}">${plant.Naam}</option>`;
  }
  html += '<select>';
  htmlPlantWater.innerHTML = html;
  htmlPlantTimer.innerHTML = html;
};

//#endregion

//#region ***  Data Access - get___                     ***********
const getDataTemp = function (sensor_id) {
  sensor_id = htmlTemplive.getAttribute('data-sensorid');
  handleData(`http://${lanIP}/api/v1/DeviceLog/${sensor_id}`, showDataTemp, null, 'GET');
};
const getDataLdr = function (sensor_id) {
  sensor_id = htmlLDRlive.getAttribute('data-sensorid');
  handleData(`http://${lanIP}/api/v1/DeviceLog/${sensor_id}`, showDataLdr, null, 'GET');
};
const getDataMoisture = function (sensor_id) {
  sensor_id = htmlMoisturelive.getAttribute('data-sensorid');
  handleData(`http://${lanIP}/api/v1/DeviceLog/${sensor_id}`, showDataMoisture, null, 'GET');
};

const getUpdatedDataTemp = function (sensor_id) {
  sensor_id = htmlTemplive.getAttribute('data-sensorid');
  handleData(`http://${lanIP}/api/v1/DeviceLog/${sensor_id}`, showUpdatedDataTemp, null, 'GET');
};
const getUpdatedDataLdr = function (sensor_id) {
  sensor_id = htmlLDRlive.getAttribute('data-sensorid');
  handleData(`http://${lanIP}/api/v1/DeviceLog/${sensor_id}`, showUpdatedDataLdr, null, 'GET');
};
const getUpdatedDataMoisture = function (sensor_id) {
  sensor_id = htmlMoisturelive.getAttribute('data-sensorid');
  handleData(`http://${lanIP}/api/v1/DeviceLog/${sensor_id}`, showUpdatedDataMoisture, null, 'GET');
};
const showTimer = function (data) {
  console.log(data);
};

const showTimerMoisture = function (data) {
  console.log(data);
};
const getLdrLog = function (sensor_id) {
  sensor_id = 1;
  handleData(`http://${lanIP}/api/v1/DeviceLog/Sensor/${sensor_id}`, showLogLdr, null, 'GET');
};
const getMoistureLog = function (sensor_id) {
  sensor_id = 2;
  handleData(`http://${lanIP}/api/v1/DeviceLog/Sensor/${sensor_id}`, showLogMoisture, null, 'GET');
};
const getTempLog = function (sensor_id) {
  sensor_id = 3;
  handleData(`http://${lanIP}/api/v1/DeviceLog/Sensor/${sensor_id}`, showLogTemp, null, 'GET');
};

const getPlants = function () {
  handleData(`http://${lanIP}/api/v1/Plants`, showSelectPlant, null, 'GET');
};

const getTimer = function () {
  handleData(`http://${lanIP}/api/v1/Timer`, showTimer, null, 'GET');
};
const getTimerMoisture = function () {
  handleData(`http://${lanIP}/api/v1/TimerMoisture`, showTimerMoisture, null, 'GET');
};
//#endregion
const init = function () {
  htmlData = document.querySelector('.js-table');
  htmlHome = document.querySelector('.js-home');
  htmlOverview = document.querySelector('.js-overview');
  htmlTemplive = document.querySelector('.js-charttemp');
  htmlLDRlive = document.querySelector('.js-chartldr');
  htmlMoisturelive = document.querySelector('.js-chartmoist');
  htmlTempLog = document.querySelector('.js-temperature');
  htmlLdrLog = document.querySelector('.js-ldr');
  htmlMoistureLog = document.querySelector('.js-moisture');
  htmlIrrigation = document.querySelector('.js-irrigation');
  htmlPlantWater = document.querySelector('.js-plant-water');
  htmlPlantTimer = document.querySelector('.js-plant-timer');
  htmlTimer = document.querySelector('.js-addtimer');
  if (htmlHome) {
    console.log('About Page');
  }
  if (htmlOverview) {
    console.log('Overview Page');
    getDataTemp();
    // getDataTemp();
    getDataLdr();
    getDataMoisture();
  }
  if (htmlLdrLog) {
    getLdrLog();
  }
  if (htmlMoistureLog) {
    getMoistureLog();
  }
  if (htmlTempLog) {
    getTempLog();
  }
  if (htmlIrrigation) {
    getPlants();
    listenToClickBtnWater();
    listenToClickBtnTimer();
    getTimer();
    getTimerMoisture();
  }
};
document.addEventListener('DOMContentLoaded', function () {
  console.log('document geladen');
  init();
  listenToSocket();
});
