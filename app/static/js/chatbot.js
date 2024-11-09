let chatbot_popup_close_button = document.querySelector(".popup-close-button");
let chatbot_minimised_elem = document.querySelector(".chatbot-minimised");
let chatbot_popup_elem = document.querySelector(".chatbot-popup");

let prompt_input = document.querySelector(".prompt");
let prompt_form = document.querySelector(".prompt-form");
let sample_message = document.querySelector(".sample-message");
let messages_container = document.querySelector(".messages-container");

function append_new_message(speaker, message_body, style_class) {
  let new_message = sample_message.cloneNode(true);
  messages_container.appendChild(new_message);

  let speaker_elem = new_message.querySelector(".speaker");
  speaker_elem.innerText = speaker;

  let message_body_elem = new_message.querySelector(".message-body");
  message_body_elem.innerHTML = message_body;

  new_message.classList.add("message");
  new_message.classList.add(style_class);
  new_message.classList.remove("d-none");
  new_message.classList.remove("sample-message");

  new_message.scrollIntoView({behavior: "smooth"});
}

function send_prompt(prompt_string) {
  let form_data = new FormData();
  form_data.set("prompt", prompt_string);
  fetch("/chatbot/new_message", { method: "post", body: form_data })
  .then(response => response.json())
  .then(list_of_replies => {
    for (let i of list_of_replies) {
      append_new_message("Chatbot", i, "chatbot-message");
    }
  });
}

function minimise_chatbot_popup() {
  chatbot_popup_elem.classList.add("shrink");
  setTimeout(() => {
    chatbot_popup_elem.classList.add("d-none");
    chatbot_minimised_elem.classList.remove("d-none");
  }, 600);
}

function open_chatbot_popup() {
  chatbot_minimised_elem.classList.add("d-none");
  chatbot_popup_elem.classList.remove("d-none");
  setTimeout(() => chatbot_popup_elem.classList.remove("shrink"), 100);
}

prompt_form.addEventListener("submit", (e) => {
  e.preventDefault();
  let prompt_string = prompt_input.value;
  append_new_message("You", prompt_string, "user-message");
  send_prompt(prompt_string);
});

chatbot_minimised_elem.addEventListener("click", () => {
  open_chatbot_popup();
});

chatbot_popup_close_button.addEventListener("click", () => {
  minimise_chatbot_popup();
});
