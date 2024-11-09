// Change Quantity
let rmv1btns = document.getElementsByClassName('rmv');
let add1btns = document.getElementsByClassName('add');
let quans = document.getElementsByClassName('item_quan');
let items = document.getElementsByClassName('inputItems');
let selectItems = document.getElementsByClassName('inputItems');

const get_product_quantity = (rowNum, orderid) => {
    let itemSelect = document.getElementById(`inputItems${rowNum}`)
    let stockLimit = itemSelect.options[itemSelect.options.selectedIndex].id;
    let selectedItemProdId = itemSelect.options[itemSelect.options.selectedIndex].value
    let thisQuan = 0;
    let currentQuan = 0;
    let rows = document.getElementsByClassName(`itemRow${orderid}`);

    for (let i = 0; i < rows.length; i++) {
        let items = document.getElementById(`inputItems${orderid}_${i+1}`)

        if (items == itemSelect) {
            let quan = document.getElementById(`item_quan${orderid}_${i+1}`).value
            thisQuan += Number(quan);
            continue
        }

        if (items.options[items.options.selectedIndex].value == selectedItemProdId) {
            let quan = document.getElementById(`item_quan${orderid}_${i+1}`).value
            currentQuan += Number(quan)
        }
    }

    stockLimit -= currentQuan

    manipulateOpt(stockLimit, thisQuan, rowNum, orderid)

    return stockLimit
}

const manipulateOptCloned = (orderid, rowCounter) => {
    let rows = document.getElementsByClassName(`itemRow${orderid}`);
    let itemSelect = document.getElementById(`inputItems${orderid}_${rowCounter}`);

    items_n_quans = {};
    prod_n_max = {};

    for (let i = 0; i < rows.length; i++) {
        let row = rows[i];
        let item = row.getElementsByTagName('select')[0];
        let quan = Number(row.getElementsByTagName('input')[0].value);
        let stockLimit = Number(item.options[item.options.selectedIndex].id);
        let prod = item.options[item.options.selectedIndex].value;
        
        if (prod in items_n_quans) {
            items_n_quans[prod] += quan;
        }
        else {
            items_n_quans[prod] = quan;
        }

        prod_n_max[prod] = stockLimit;
    }

    let row = rows[rowCounter-1];
    let item = row.getElementsByTagName('select')[0];

    for (const prod of Object.keys(items_n_quans)) {

        if (items_n_quans[prod] == prod_n_max[prod] && item == itemSelect) {
            for (let i = 0; i < item.length; i++) {
                if (item.options[i].value == prod) {
                    item.remove(i);
                }
            }
        }

    }
}

const manipulateOpt = (stockLimit, thisQuan, rowNum, orderid) => {
    let items = document.getElementsByClassName(`inputItems${orderid}`)
    let itemSelect = document.getElementById(`inputItems${rowNum}`)
    let selectedItemProdId = itemSelect.options[itemSelect.options.selectedIndex].value
    let selectedItemName = itemSelect.options[itemSelect.options.selectedIndex].text

    for (let i = 0; i < items.length; i++) {
        let item = items[i]

        if (stockLimit <= 0 || stockLimit < thisQuan) {
            for (let j = 0; j < item.length; j++) {
                if (item.options[j].value == selectedItemProdId && item != itemSelect) {
                    item.remove(j);

                    if (orderid == undefined) {
                        let opt = document.createElement('option');
                        opt.id = 99;
                        opt.text = 'Choose...';
                        opt.selected = true;
                        item.add(opt);
                    } 
                }
            }
        } 
        else {
            opt_exist = false
            for (let j = 0; j < item.length; j++) {
                if (item.options[j].value == selectedItemProdId) {
                    opt_exist = true;
                }
            }
            if (!opt_exist) {
                let opt = document.createElement('option');
                opt.value = selectedItemProdId;
                opt.id = itemSelect.options[itemSelect.options.selectedIndex].id;
                opt.text = selectedItemName;
                item.add(opt);
            }
        }
    }
}

for (let i = 0; i < rmv1btns.length; i++) {

    let rmv1btn = rmv1btns[i]
    let add1btn = add1btns[i]
    let quan = Number(quans[i].value)
    let selectItem = selectItems[i]

    // Reset Quantity on change select
    selectItem.addEventListener('change', () => {
        quan = 1;
        quans[i].value = quan;
        add1btn.disabled = false;
        add1btn.classList.remove('disabled-btn');
        rmv1btn.disabled = false;
        rmv1btn.classList.add('disabled-btn');
    })

    rmv1btn.addEventListener('click', (e) => {

        e.preventDefault();
        e.stopPropagation();

        let sameItemAdd = [];
        let sameItemRmv = [];

        let itemNum = e.target.attributes.id.value.split('_')[1];

        orderid = e.target.form[0].attributes.value
        if (orderid != undefined) {
            orderid = orderid.value;
        }
        let rowNum = `${orderid}_${itemNum}`;

        let allItems = document.getElementsByClassName(`itemRow${orderid}`);
        let itemSelect = document.getElementById(`inputItems${orderid}_${itemNum}`);

        for (let i = 0; i < allItems.length; i++) {
            let items = document.getElementById(`inputItems${orderid}_${i+1}`);
    
            if (items.options[items.options.selectedIndex].value == itemSelect.options[itemSelect.options.selectedIndex].value) {
                sameItemAdd.push(allItems[i].querySelector('.add'));
                sameItemRmv.push(allItems[i].querySelector('.rmv'));
            }
            
        }

        if (quan <= 1) {
            rmv1btn.disabled = true;
            rmv1btn.classList.add('disabled-btn');
            return
        }
        else {
            quan -= 1;
            quans[i].value = quan;

            if (quan <= 1) {
                rmv1btn.disabled = true;
                rmv1btn.classList.add('disabled-btn');
            }

            if (quan <= get_product_quantity(rowNum, orderid)) {
                sameItemAdd.forEach((btn) => {
                    btn.disabled = false;
                    btn.classList.remove('disabled-btn');
                })
            }

            return
        }
    })

    add1btn.addEventListener('click', (e) => {

        e.preventDefault();
        e.stopPropagation();

        let sameItemAdd = [];
        let sameItemRmv = [];

        let itemNum = e.target.attributes.id.value.split('_')[1];

        orderid = e.target.form[0].attributes.value
        if (orderid != undefined) {
            orderid = orderid.value;
        }
        let rowNum = `${orderid}_${itemNum}`;

        let allItems = document.getElementsByClassName(`itemRow${orderid}`);
        let itemSelect = document.getElementById(`inputItems${orderid}_${itemNum}`);

        for (let i = 0; i < allItems.length; i++) {
            let items = document.getElementById(`inputItems${orderid}_${i+1}`);
    
            if (items.options[items.options.selectedIndex].value == itemSelect.options[itemSelect.options.selectedIndex].value) {
                sameItemAdd.push(allItems[i].querySelector('.add'));
                sameItemRmv.push(allItems[i].querySelector('.rmv'));
            }
            
        }

        quan += 1;
        quans[i].value = quan;

        if (quan > 1) {
            rmv1btn.disabled = false
            rmv1btn.classList.remove('disabled-btn')
        }

        if (quan >= get_product_quantity(rowNum, orderid)) {
            sameItemAdd.forEach((btn) => {
                btn.disabled = true
                btn.classList.add('disabled-btn')
            })
        }

        return
    })

}

// Add Item Row
let itemRows = document.getElementsByClassName('itemRow');
let addRowBtns = document.getElementsByClassName('add_prods_row');
let counter = 1;

// Change Quantity for new rows
for (let i = 0; i < addRowBtns.length; i++) {

    let addRow = addRowBtns[i]
    let itemRow = itemRows[i]

    addRow.addEventListener('click', (e) => {

        orderid = e.target.form[0].attributes.value

        counter++;

        e.preventDefault();
        e.stopPropagation();

        let clone = itemRow.cloneNode(true)
        let rowNum = `${orderid}_${counter}`

        let select = clone.getElementsByTagName('select')[0]
        let rmv = clone.getElementsByTagName('button')[0]
        let add = clone.getElementsByTagName('button')[1]

        // Reset Quantity for new row
        let quan = 1
        add.disabled = false;
        add.classList.remove('disabled-btn');
        rmv.disabled = false;
        rmv.classList.add('disabled-btn');

        select.id = `inputItems${orderid}_${counter}`;
        select.name = `items${orderid}_${counter}`;
        clone.getElementsByTagName('input')[0].value = 1;
        clone.getElementsByTagName('input')[0].id = `item_quan${orderid}_${counter}`;
        clone.getElementsByTagName('input')[0].name = `quantity${orderid}_${counter}`;
        clone.getElementsByTagName('input')[1].name = `requests${orderid}_${counter}`;

        rmv.id = `rmv${orderid}_${counter}`;
        add.id = `add${orderid}_${counter}`;

        clone.classList.add('mt-2')
        clone.id = `itemRow${orderid}_${counter}`;''

        // Reset Quantity on change select
        select.addEventListener('change', () => {
            quan = 1;
            clone.getElementsByTagName('input')[0].value = quan;
            add.disabled = false;
            add.classList.remove('disabled-btn');
            rmv.disabled = false;
            rmv.classList.add('disabled-btn');
        })

        let rmvRow = document.createElement('button')
        rmvRow.textContent = 'x'
        rmvRow.classList = 'remove_row col-md-1'

        rmvRow.addEventListener('click', (e) => {

            // Disable Default
            e.preventDefault();
            e.stopPropagation();
    
            // Delete Row
            let row = document.getElementById(e.target.parentNode.id);
            row.parentNode.removeChild(row);
            counter--;
            
            return
        })

        clone.appendChild(rmvRow)

        rmv.addEventListener('click', (e) => {
            
            e.preventDefault();
            e.stopPropagation();

            let sameItemAdd = [];
            let sameItemRmv = [];

            let allItems = document.getElementsByClassName(`itemRow${orderid}`);
            let itemSelect = document.getElementById(`inputItems${rowNum}`);

            for (let i = 0; i < allItems.length; i++) {
                let items = document.getElementById(`inputItems${orderid}_${i+1}`);
        
                if (items.options[items.options.selectedIndex].value == itemSelect.options[itemSelect.options.selectedIndex].value) {
                    sameItemAdd.push(allItems[i].querySelector('.add'));
                    sameItemRmv.push(allItems[i].querySelector('.rmv'));
                }
                
            }
        
            if (quan <= 1) {
                rmv.disabled = true;
                rmv.classList.add('disabled-btn');
                return
            }
            else {
                quan -= 1;
                clone.getElementsByTagName('input')[0].value = quan;
        
                if (quan <= 1) {
                    rmv.disabled = true;
                    rmv.classList.add('disabled-btn');
                }

                if (quan <= get_product_quantity(rowNum, orderid)) {
                    sameItemAdd.forEach((btn) => {
                        btn.disabled = false;
                        btn.classList.remove('disabled-btn');
                    })
                }
        
                return
            }
        })

        add.addEventListener('click', (e) => {

            e.preventDefault();
            e.stopPropagation();

            let sameItemAdd = [];
            let sameItemRmv = [];

            let allItems = document.getElementsByClassName(`itemRow${orderid}`);
            let itemSelect = document.getElementById(`inputItems${rowNum}`);

            for (let i = 0; i < allItems.length; i++) {
                let items = document.getElementById(`inputItems${orderid}_${i+1}`);
        
                if (items.options[items.options.selectedIndex].value == itemSelect.options[itemSelect.options.selectedIndex].value) {
                    sameItemAdd.push(allItems[i].querySelector('.add'));
                    sameItemRmv.push(allItems[i].querySelector('.rmv'));
                }
                
            }
        
            quan += 1;
            clone.getElementsByTagName('input')[0].value = quan;
        
            if (quan > 1) {
                rmv.disabled = false
                rmv.classList.remove('disabled-btn')
            }
        
            if (quan >= get_product_quantity(rowNum, orderid)) {
                sameItemAdd.forEach((btn) => {
                    btn.disabled = true
                    btn.classList.add('disabled-btn')
                })
            }
        
            return
        })

        itemRow.parentNode.appendChild(clone);

        manipulateOptCloned(orderid, counter)

        return
    })
}

// Validation (Cannot use WTForms as it refreshes page and get rids of HTML manipulation)
const validateFields = (form) => {

    let inputs = form.getElementsByTagName('input');
    let select = form.getElementsByTagName('select');
    
    let valid_disc = inputs[inputs.length - 2].value
    let valid_items = inputs[inputs.length - 1].value
    let valid_countries = ['Singapore', 'Sweden'];
    let valid_codes = ['+65', '+46'];
    let valid_status = ['Pending', 'Production', 'Dispatched']

    let errors = 0;

    // Inputs
    for (let i=0; i < inputs.length; i++) {

        let input = inputs[i];
        
        // Optional Fields
        if (input.name.includes('requests') || input.name.includes('notes') || input.name.includes('validDisc') || input.name.includes('validProducts')) {
            continue
        }

        // General
        if ((!input.value || input.value == "") && !(input.name.includes('discount'))) {
            input.classList.add('invalidField')
            errors += 1;
            continue
        } 

        // Quanity
        if (input.name.includes('quantity')) {
            let rowID = input.id
            let rowNum = rowID.slice(9)
            let itemSelect = document.getElementById(`inputItems${rowNum}`)
            let stockLimit = itemSelect.options[itemSelect.options.selectedIndex].id;

            if (input.value < 1 || input.value > stockLimit || !Number(input.value)) {
                input.classList.add('invalidField')
                errors += 1;
                continue
            }
        }

        // Contact Number
        if (input.name.includes("cnumber")) {
            let re = /^[0-9]*$/
            if (!re.test(input.value) || input.value.length != 8) {
                input.classList.add('invalidField')
                errors += 1;
                continue
            }
        }

        // Email
        let re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (input.name.includes('email') && !re.test(input.value)) {
            input.classList.add('invalidField')
            errors += 1;
            continue
        }

        // Discount Code
        if (input.name.includes('discount')) {
            if (input.value == "") {
                continue
            }

            if ((!valid_disc.includes(input.value))) {
                input.classList.add('invalidField')
                errors += 1;
                continue
            }
        }

        input.classList.remove('invalidField')
    }

    // Selects
    for (let i=0; i < select.length; i++) {

        let input = select[i];

        // General
        if (!input.value || input.value == "") {
            input.classList.add('invalidField')
            errors += 1;
            continue
        }

        // Items
        if (input.name.includes('items')) {
            if (!(valid_items.includes(input.value))) {
                input.classList.add('invalidField')
                errors += 1;
                continue
            }
        }

        // Country
        if (input.name.includes('country')) {
            if (!(valid_countries.includes(input.value))) {
                input.classList.add('invalidField')
                errors += 1;
                continue
            }
        }

        // Contact Number Country Code
        if (input.name.includes('cCode')) {
            if (!(valid_codes.includes(input.value))) {
                input.classList.add('invalidField')
                errors += 1;
                continue
            } 
        }

        // Status
        if (input.name.includes('status')) {
            if (!(valid_status.includes(input.value))) {
                input.classList.add('invalidField')
                errors += 1;
                continue
            } 
        }

        input.classList.remove('invalidField')

    }

    if (errors == 0) {
        return true
    }

    return false
}

// Submit for Create
submitBtn = document.getElementById('submitBtn');

submitBtn.addEventListener('click', (e) => {

    form = document.getElementById('createForm')

    if (!validateFields(form)) {
        e.preventDefault();
        e.stopPropagation();
    } 
    
})

// Submit for Update
submitBtns = document.getElementsByClassName('submitBtns')

for (let i = 0; i < submitBtns.length; i++) {
    submitBtn = submitBtns[i]

    submitBtn.addEventListener('click', (e) => {

        if (validateFields(form)) {
            form.submit()
        } 
        else {
            e.preventDefault();
            e.stopPropagation();
        }

    })
}