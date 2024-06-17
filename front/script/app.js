const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

const sendAddData = () => {
  const textareaValue = document.getElementById('courseData').value;
  console.info(textareaValue)
  socketio.emit('B2F_addCourse', {
      coursedata: textareaValue
  });
}

const listenToUI = () => {};

const listenToSocket = () => {
  socketio.on('connect', function () {
    console.info('verbonden met socket webserver');
  });

  socketio.on('B2F_history', function (jsonObject) {
    console.info('history');
    console.info(jsonObject);
    displayHistoryData(jsonObject.history)
    window.scrollTo(0, document.body.scrollHeight);
  });

  socketio.on('B2F_success', function () {
    location.href = "index.html"
  });
};

const displayHistoryData = (historyArray) => {
  let htmlString = `
  <tr>
    <th>ID</th>
    <th>Device</th>
    <th>Action</th>
    <th>Parameters</th>
    <th>Elapsed</th>
  </tr>
  `;

  for (let item of historyArray) {
    htmlString += `
    <tr>
      <td>${item.device_id}</td>
      <td>piezo</td>
      <td>hit${item.action_id}</td>
      <td>${item.parameters}</td>
      <td>00:04:20:30 ${Date.parse(item.timestamp)}</td>
    </tr>
    `;
  }
  document.querySelector('.js-history-table').innerHTML = htmlString;
};

const init = () => {
  console.info('DOM geladen');
  listenToUI();
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);
