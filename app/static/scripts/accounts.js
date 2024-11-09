function search() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[1];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

function others(){
  let position = document.getElementById('position')
  let others_elem = document.getElementById('others')
  console.log(position.value)
  if (position.value == 'Others'){
    others_elem.style.display = 'block'
  }else{
    others_elem.style.display = "none"
  }
}

document.addEventListener("DOMContentLoaded", () => others());
document.addEventListener("DOMContentLoaded", () => {
  let others_elem = document.querySelector("#position");
  others_elem.addEventListener("click", () => others());
});