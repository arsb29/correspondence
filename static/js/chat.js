const message_replies = document.querySelectorAll('div.message_reply');
const form_blockquote = document.querySelector('#form_blockquote');
const submitMessage = document.querySelector('#submitMessage');
const chatSectionFeed = document.querySelector('.chat-section__feed');

function deleteBlockquote() {
    form_blockquote.innerText = "";
    form_blockquote.setAttribute('data-id', "");
}

form_blockquote.addEventListener('click', deleteBlockquote)

function replyFunction() {
    parentElement = this.parentElement
    form_blockquote.innerHTML = parentElement.querySelector(".message__content > p").innerHTML;
    form_blockquote.setAttribute('data-id', this.getAttribute('data-id'));
    form_blockquote.scrollIntoView();
}

for (let i = 0; i < message_replies.length; i++) {
    message_replies[i].addEventListener('click', replyFunction);
}

let form;
function findElements() {
    form = document.querySelector('form');
}
function showMessage(data) {
    alert(data);
}
function onSuccess(response) {
    return response.json()
        .then(res => {
            const {
                author_id,
                avatar_file_id,
                created_date,
                lastName,
                message_id,
                name,
                photos,
                reply_id,
                reply_text,
                text,
                document_id
            } = res.message;
            const origin_document = `<a class="message__doc-link" href="/file/${document_id}">
                    <span class="message__doc-icon">
                        <img alt="" height="28" src="/static/images/doc.svg" width="22">
                    </span>
                    <span class="message__doc-label">Оригинал документа</span>
                </a>`;
            const photosElement = document.createElement("div");
            photosElement.classList.add('message__previews');
            for (let i = 0; i < photos.length; i++) {
                photosElement.innerHTML += `
                    <a class="message__preview js-gallery-slide" data-lightbox="gallery${message_id}" href="/file/${photos[i]}">
                        <img alt="" width="25" height="25" src="/file/${photos[i]}">
                    </a>`;
            }
            const avatar = avatar_file_id ? `/file/${avatar_file_id}` : "/static/images/avatar.png";
            const mes_reply = document.createElement('blockquote');
            mes_reply.innerHTML = `<blockquote className="message__quote">${reply_text}</blockquote>`;
            const mes = document.createElement("div");
            mes.classList.add('chat-section__message');
            mes.innerHTML = `<div class="chat-section__message">
                <div class="message message_outcoming">
                    <a class="message__avatar" href="">
                        <img alt="" src="${avatar}">
                    </a>
                    <div class="message__body">
                        <div class="message__header">
                            <div class="message__author">
                                <a class="message__author-name js-name" href="#">${name} ${lastName}</a>
                            </div>
                        </div>
                        <div class="message__content">
                            ${reply_text ? mes_reply.innerHTML : ''}
                            <p>${text}</p>
                        </div>
                        <div class="message__footer">
                            ${document_id ? origin_document : ''}                     
                            ${photos ? photosElement.innerHTML : ''}                            
                            <div class="message__date">${created_date}</div>
                        </div>
                    </div>
                </div>
                <div class="message_reply" data-id="${message_id}">Ответить</div>
            </div>`;
            mes.querySelector('div.message_reply').addEventListener('click', replyFunction);
            chatSectionFeed.appendChild(mes);
            form.reset();
            deleteBlockquote();
        });
}

function onError(data) {
    showMessage(data);
}
function collectData(currentForm) {
    const data = new FormData(currentForm);
    let countPhotos = 0;
    for(let [name, value] of data) {
        if (name === 'photos') {
            countPhotos += 1;
            data.append(`photos${countPhotos}`, value);
        }
    }
    data.append('countPhotos', countPhotos);
    data.delete('photos');
    data.append('reply_message_id', Number(form_blockquote.getAttribute('data-id')));
    return data;
}
function setOptions(currentForm) {
  return {
    method: 'post',
    body: collectData(currentForm)
  };
}
function sendForm(currentForm) {
  return fetch(document.location.href, setOptions(currentForm));
}
function onSubmit(event) {
    event.preventDefault();
    const { currentTarget } = event;
    submitMessage.disabled = true;
    submitMessage.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Загрузка';
    sendForm(currentTarget)
        .then(response => onSuccess(response, currentTarget))
        .catch(onError)
        .finally(() => {
            submitMessage.disabled = false;
            submitMessage.innerHTML = 'Отправить';
        });
}
function subscribe() {
  form.addEventListener('submit', onSubmit);
}
function init() {
  findElements();
  subscribe();
}
init();

const addUser = document.querySelector('#addUser');
const datalistOptions = document.querySelector('#datalistOptions');
const exampleDataList = document.querySelector('#exampleDataList');
const listChatUsers = document.querySelector('#listChatUsers');

function fetchChatUsers() {
    return fetch(`${document.location.href}/users`)
        .then(res => res.json())
        .then(res => {
            const {not_chat_users, chat_users} = res;
            datalistOptions.innerHTML = '';
            for (let i = 0; i < not_chat_users.length; i++) {
                datalistOptions.innerHTML += `<option value="${not_chat_users[i].login}" label="${not_chat_users[i].name} ${not_chat_users[i].lastName}">`
            }

            listChatUsers.innerHTML = '';
            for (let i = 0; i < chat_users.length; i++) {
                listChatUsers.innerHTML += `<li class="list-group-item">@${chat_users[i].login} ${chat_users[i].name} ${chat_users[i].lastName}</li>`
            }
        })
        .catch(onError)
}
fetchChatUsers()


function fetchAddUser() {
    let formData = new FormData();
    formData.append('login', exampleDataList.value);
    return fetch(`${document.location.href}/users`, {
        method: 'post',
        body: formData
    })
}

function addUserFunction() {
    fetchAddUser()
        .then(res => res.json())
        .then(res => {
            const mes = document.createElement("div");
            mes.classList.add('chat-section__notify');
            mes.innerHTML = `<div class="notify"><p>${res.message}</p></div>`;
            chatSectionFeed.appendChild(mes);
            return fetchChatUsers()
        })
        .then(res => {
            exampleDataList.value = '';
        })
}

addUser.addEventListener('click', addUserFunction)