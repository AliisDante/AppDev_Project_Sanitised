// Sorting Table
function sortTable(option) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("myTable0");
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      if (option ==0){
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      document.getElementById("sort").innerHTML = "Sort by: ID";
      }
      if (option ==1){
      x = rows[i].getElementsByTagName("TD")[1];
      y = rows[i + 1].getElementsByTagName("TD")[1];
      document.getElementById("sort").innerHTML = "Sort by: Alphabetical";
      }
      if (option ==2){
      x = rows[i].getElementsByTagName("TD")[3];
      y = rows[i + 1].getElementsByTagName("TD")[3];
      document.getElementById("sort").innerHTML = "Sort by: Quantity";
      }
      if (option ==3){
      x = rows[i].getElementsByTagName("TD")[2];
      y = rows[i + 1].getElementsByTagName("TD")[2];
      document.getElementById("sort").innerHTML = "Sort by: Type";
      }
      if (option ==4){
      x = rows[i].getElementsByTagName("TD")[4];
      y = rows[i + 1].getElementsByTagName("TD")[4];
      document.getElementById("sort").innerHTML = "Sort by: Date Submitted";
      }
      if (option ==6){
      x = rows[i].getElementsByTagName("TD")[6];
      y = rows[i + 1].getElementsByTagName("TD")[6];
      document.getElementById("sort").innerHTML = "Sort Status by : OPEN";
      }
      if (option ==0 || option== 1){
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
      if (option ==2){
        if (Number(x.innerHTML) > Number(y.innerHTML)) {
          shouldSwitch = true;
          break;
        }
      }
      if (option ==3){
        if (x.innerHTML > y.innerHTML) {
          shouldSwitch = true;
          break;
        }
      }
      if (option == 4){
        if (x.innerHTML > y.innerHTML) {
          shouldSwitch = true;
          break;
        }
      }
      if (option == 6){
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}
//filter table
function filter_Table(option){
    let rows = document.getElementById("myTable0").rows
    for(let i=1;i<rows.length;i++){
        let row_ele = rows[i].getElementsByTagName("TD")
        rows[i].style.display="table-row"
        if(option ==-1){
            rows[i].style.display="table-row"
            document.getElementById("filter").innerHTML = "Filter by:"
        }
        else if(option ==0){
            if(row_ele[2].innerHTML !== "B"){
                rows[i].style.display = "none"
                document.getElementById("filter").innerHTML = "Filter by: Type Bedding"
        }
        }
        else if(option ==1){
            if(row_ele[2].innerHTML !== "H"){
                rows[i].style.display = "none"
                document.getElementById("filter").innerHTML = "Filter by: Type Housing"
        }
        }
        else if(option ==2){
            if(row_ele[2].innerHTML !== "D"){
                rows[i].style.display = "none"
                document.getElementById("filter").innerHTML = "Filter by: Type Dining"
        }
        }
        else if(option ==3){
            if(row_ele[2].innerHTML !== "L"){
                rows[i].style.display = "none"
                document.getElementById("filter").innerHTML = "Filter by: Type Living"
        }
        }
        else if(option ==4){
            if(row_ele[3].innerHTML >10 ){
                rows[i].style.display = "none"
                document.getElementById("filter").innerHTML = "Filter by: Low Quantity (0-10)"
        }
        }
        else if(option ==5){
            if(row_ele[3].innerHTML <10 || row_ele[3].innerHTML >50){
                rows[i].style.display = "none"
                document.getElementById("filter").innerHTML = "Filter by: Moderate Quantity (11-50)"
        }
        }
        else if(option ==6){
            if(row_ele[3].innerHTML < 51){
                rows[i].style.display = "none"
                document.getElementById("filter").innerHTML = "Filter by: High Quantity (>50)"
        }

        }
        else if(option ==7){
            if(row_ele[4].innerHTML !== "Waiting"){
                rows[i].style.display = "none"
                document.getElementById("filter").innerHTML = "Filter by: Waiting Restock Status"
                console.log(row_ele[4].innerHTML)
        }else{

        }
        }


    }
}




//Search Table
function getRowText(table_row_elem) {
    const table_row_id_elem = table_row_elem.querySelector(".product-id");
    const table_row_name_elem = table_row_elem.querySelector(".product-name");
    let textToSearch = table_row_id_elem.innerText + table_row_name_elem.innerText;
    return textToSearch;
}

function searchTable(text) {
    const myTable = document.getElementById("myTable");
    let product_rows = document.querySelectorAll(".product-row");
    for (let i of product_rows) {
        if (!getRowText(i).toLowerCase().includes(text.toLowerCase())) {
            i.classList.add("d-none");
        }

        else {
            i.classList.remove("d-none");
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    let searchElement = document.getElementById("myInput");
    searchElement.addEventListener("input", (e) => {
        searchTable(e.target.value);
    })
})


//Showing image in form
function getImgData() {
  var file = document.getElementById("picture_1").files[0];
  var allowedExtension = ['jpeg', 'jpg','png','gif'];
  var filename = file.name
  var fileExtension = document.getElementById('picture_1').value.split('.').pop().toLowerCase();
  var isValid = false
    if (file) {
        for(let index in allowedExtension){
            if(fileExtension === allowedExtension[index]){
                isValid = true
                const fileReader = new FileReader();
                fileReader.readAsDataURL(file);
                fileReader.addEventListener("load", function () {
                document.getElementById("img-preview").innerHTML = '<img src="' + this.result + '" />';
                document.getElementById("img-preview").innerHTML += `<p>File Name Chosen: ${filename}</p>`
                document.getElementById("img-preview").childNodes[1].style.width = "200%";
                });
                }
  }
  }
    if(!isValid){
        document.getElementById("img-preview").innerHTML = '<img src="/static/images/Invalid File.png" />';
        document.getElementById("img-preview").innerHTML += `<p>File Chosen: ${filename}</p>`;
        document.getElementById("img-preview").childNodes[1].style.width = "200%"
      }
}
//Resetting image and file name chosen
function resetImgData(){
    document.getElementsByTagName("img")[2].src = "/static/images/blank_img.png"
    document.getElementById("img-preview").childNodes[1].remove()
}

//image validation messages
function validateFile(option)
        {

            var allowedExtension = ['jpeg', 'jpg','png','gif'];
            var fileExtension = document.getElementById('picture_1').value.split('.').pop().toLowerCase();
            var isValidFile = false;
            if(option==1 && fileExtension==""){
                return true
                }
                if(option == 0){
                if(fileExtension == ""){
                    document.getElementById("ImgPresenceError").style.display = "list-item"
                                        }
                else{
                    document.getElementById("ImgPresenceError").style.display = "none"
                    }
                                }

                for(var index in allowedExtension) {

                    if(fileExtension === allowedExtension[index]) {
                        isValidFile = true;
                        break;
                    }
                }

                if(!isValidFile) {
                    document.getElementById("ImgFormatError").style.display = "list-item"
                }


                return isValidFile;
        }


