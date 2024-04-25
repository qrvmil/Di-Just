chrome.runtime.onInstalled.addListener(function() {
  // Создаем контекстное меню для изображений
  chrome.contextMenus.create({
    title: "Добавить в дайджест",
    contexts: ["image"],
    id: "addToDigestImage"
  });

  // Создаем контекстное меню для ссылок
  chrome.contextMenus.create({
    title: "Добавить в дайджест",
    contexts: ["link"],
    id: "addToDigestLink"
  });
});

// Обработчик кликов на контекстное меню
chrome.contextMenus.onClicked.addListener(function(info, tab) {
  if (info.menuItemId === "addToDigestImage" || info.menuItemId === "addToDigestLink") {
    // Показываем окно с кнопками дайджестов
    showDigestList(info.srcUrl || info.linkUrl, info.menuItemId);
  }
});

// Функция для получения токена из cookies
function getToken(callback) {
  const serverUrl = 'URL_SERVER';
  chrome.cookies.get({ url: serverUrl, name: 'yourTokenCookieName' }, function(cookie) {
    const token = cookie ? cookie.value : null;
    callback(token);
  });
}

// Функция для отображения окна с кнопками дайджестов
function showDigestList(content, contextMenuId) {
  getToken(function(token) {
    if (!token) {
      console.error('Не удалось получить токен из cookies.');
      return;
    }

    // Здесь вы можете получить список дайджестов с сервера
    // и построить окно с кнопками, а затем отправить запрос обновления дайджеста
    // В этом примере просто выводим alert с выбранным дайджестом

    const digests = ["Digest1", "Digest2", "Digest3"]; // Замените этот массив на реальный список дайджестов

    const selectedDigest = prompt("Выберите дайджест:", digests.join(", "));
    if (selectedDigest && digests.includes(selectedDigest)) {
      // Отправляем запрос на сервер с выбранным дайджестом и контентом
      updateDigest(selectedDigest, content, contextMenuId, token);
    } else {
      console.log("Отменено пользователем");
    }
  });
}

// Функция для отправки запроса на сервер для обновления дайджеста
function updateDigest(digest, content, contextMenuId, token) {
  // Здесь выполните запрос на сервер для обновления дайджеста
  // Используйте fetch, добавляя заголовок Authorization с токеном

  // Замените 'URL_SERVER' на ваш реальный URL сервера
  const serverUrl = 'URL_SERVER';

  fetch(serverUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      digest: digest,
      content: content,
      contextMenuId: contextMenuId,
    }),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('Сервер ответил:', data);
  })
  .catch(error => {
    console.error('Ошибка при отправке на сервер:', error);
  });
}
