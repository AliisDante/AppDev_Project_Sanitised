let product_rows = document.querySelectorAll(".product");

for (let i of product_rows) {
  let quantity_input = i.querySelector("input[type=text]");
  let minus_button = i.querySelector("button.minus-button");
  let plus_button = i.querySelector("button.plus-button");
  let change_button = i.querySelector("button.change-button");
  let product_stock = Number(quantity_input.getAttribute("data-product-stock"));
  let max_quantity_allowed = Number(quantity_input.getAttribute("data-max-quantity-allowed"));

  function submit_product_changes() {
    i.requestSubmit(change_button);
  }

  function set_buttons() {
    minus_button.disabled = false;
    plus_button.disabled = false;

    if (quantity_input.value <= 1) {
      minus_button.disabled = true;
    }

    if (quantity_input.value >= product_stock || quantity_input.value >= max_quantity_allowed) {
      plus_button.disabled = true;
    }
  }

  minus_button.addEventListener("click", () => {
    quantity_input.value = Math.max(Number(quantity_input.value) - 1, 0);
    submit_product_changes();

    set_buttons()
  });

  plus_button.addEventListener("click", () => {
    quantity_input.value = Number(quantity_input.value) + 1;
    submit_product_changes();
    set_buttons()
  });

  set_buttons()
}
