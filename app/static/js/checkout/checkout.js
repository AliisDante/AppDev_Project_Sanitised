function input_value_is_valid(input_elem, pattern) {
  return new RegExp(pattern).test(input_elem.value);
}

function custom_validation(input_elem, pattern, message) {
  let input_name = input_elem.name;
  let input_error_elem = document.querySelector(`.${input_name}-error`);
  input_elem.addEventListener("input", () => {
    if (input_value_is_valid(input_elem, pattern)) {
      input_error_elem.innerText = "";
    } else {
      input_error_elem.innerText = message;
    }
  });
}

function expiry_date_is_valid(month_str, year_str) {
  let year = Number(`20${year_str}`);
  let month = Number(month_str);
  let expiry_date = new Date(year, month - 1);
  let current_date = /* @__PURE__ */ new Date();
  return expiry_date > current_date;
}

function expiry_date_listener() {
  let month_str = payment_expiry_date_month_input.value;
  let year_str = payment_expiry_date_year_input.value;
  let expiry_date_error_elem = document.querySelector(".payment-expiry-date-error");
  expiry_date_error_elem.innerText = "";
  if (!new RegExp("^((1[0-2])|(0[1-9]))$").test(month_str)) {
    expiry_date_error_elem.innerText = "Month should be within 01 to 12";
  } else if (!new RegExp("^\\d{2}$").test(year_str)) {
    expiry_date_error_elem.innerText = "Year should have 2 digits in the YY format";
  } else if (!expiry_date_is_valid(month_str, year_str)) {
    expiry_date_error_elem.innerText = "Expiry date has past";
  }
}

custom_validation(document.querySelector("#delivery-postal-code"), "^\\d{6}$", "Postal code should have 6 digits");
custom_validation(document.querySelector("#billing-postal-code"), "^\\d{6}$", "Postal code should have 6 digits");
custom_validation(document.querySelector("#delivery-contact-number"), "^\\d{8}$", "Contact number should have 8 digits");
custom_validation(document.querySelector("#billing-contact-number"), "^\\d{8}$", "Contact number should have 8 digits");
custom_validation(document.querySelector("#payment-card-number"), "^\\d{16}$", "Card number should have 16 digits");
custom_validation(document.querySelector("#payment-cvv"), "^\\d{3,4}$", "CVV should have 3 or 4 digits");

let payment_expiry_date_month_input = document.querySelector("#payment-expiry-date-month");
let payment_expiry_date_year_input = document.querySelector("#payment-expiry-date-year");
document.querySelector("#payment-expiry-date-month").addEventListener("input", expiry_date_listener);
document.querySelector("#payment-expiry-date-year").addEventListener("input", expiry_date_listener);

function get_delivery_and_billing_element_with_base_element_id(base_elem_id) {
  let delivery_input_elem = document.querySelector(`#delivery-${base_elem_id}`);
  let billing_input_elem = document.querySelector(`#billing-${base_elem_id}`);
  return [delivery_input_elem, billing_input_elem];
}

function get_all_delivery_and_billing_elements() {
  let all_elems = [];
  all_elems.push(get_delivery_and_billing_element_with_base_element_id("name"));
  all_elems.push(get_delivery_and_billing_element_with_base_element_id("email"));
  all_elems.push(get_delivery_and_billing_element_with_base_element_id("country-code"));
  all_elems.push(get_delivery_and_billing_element_with_base_element_id("contact-number"));
  all_elems.push(get_delivery_and_billing_element_with_base_element_id("postal-code"));
  all_elems.push(get_delivery_and_billing_element_with_base_element_id("address"));
  all_elems.push(get_delivery_and_billing_element_with_base_element_id("country"));
  return all_elems;
}

let billing_copy_from_delivery_button = document.querySelector("#billing-copy-from-delivery");
billing_copy_from_delivery_button.addEventListener("click", () => {
  let input_event = new InputEvent("input");
  for (let input_elem_array of get_all_delivery_and_billing_elements()) {
    let [delivery_input_elem, billing_input_elem] = input_elem_array;
    billing_input_elem.value = delivery_input_elem.value;
    billing_input_elem.dispatchEvent(input_event);
  }
});


let discount_code_input_elem = document.querySelector(".discount-code-input");
let discount_code_button_elem = document.querySelector(".discount-code-button");
let discount_error_elem = document.querySelector(".discount-error");
let discount_name_elem = document.querySelector(".discount-name");
let discount_amount_elem = document.querySelector(".discount-amount");

let subtotal_elem = document.querySelector(".subtotal");
let tax_elem = document.querySelector(".tax");
let total_elem = document.querySelector(".total");
function get_subtotal() {
    return subtotal_elem.getAttribute("data-subtotal");
}
function format_money(amount) {
  return `$${Number(amount).toFixed(2)}`;
}
function format_discount(type, amount) {
  if (type == "percentage") {
    return `${amount}%`;
  }
  else {
    return format_money(amount);
  }
}
function calculate_discount_amount(type, amount) {
  if (type == "percentage") {
    let subtotal = get_subtotal();
    return subtotal * (amount / 100);
  }
  else {
    return amount;
  }
}
function process_discount(discount_actual_amount) {
  let non_discounted_subtotal = get_subtotal()
  let discounted_subtotal = non_discounted_subtotal - discount_actual_amount;
  subtotal_elem.innerText = format_money(discounted_subtotal);

  let new_tax = 0.08 * discounted_subtotal;
  let new_total = discounted_subtotal + new_tax;
  tax_elem.innerText = format_money(new_tax);
  total_elem.innerText = format_money(new_total);
}

discount_code_button_elem.addEventListener("click", () => {
  let discount_code = discount_code_input_elem.value;
  let form_data = new FormData();
  form_data.set("discount-code", discount_code);
  fetch("/checkout/check_discount", {method: "post", body: form_data})
    .then((response) => {
      return response.json();
    })
    .then((discount_info) => {
      discount_error_elem.classList.remove("text-danger");
      discount_error_elem.innerText = "";
      if (discount_info.valid) {
        discount_name_elem.innerText = discount_info.name;
        discount_amount_elem.innerText = format_discount(discount_info.type, discount_info.amount);
        let discount_actual_amount = calculate_discount_amount(discount_info.type, discount_info.amount);
        process_discount(discount_actual_amount);
      } 
      else {
        discount_name_elem.innerText = "-";
        discount_amount_elem.innerText = "-";
        process_discount(0);

        discount_error_elem.innerText = "Invalid discount";
        discount_error_elem.classList.add("text-danger");
      }
    })
});
