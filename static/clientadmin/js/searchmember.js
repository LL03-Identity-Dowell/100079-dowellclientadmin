
const textArea = document.querySelector("#form-field-membersearchdetails1")
const searchInput = document.querySelector("#form-field-membersearch1")
const TableRow = document.querySelectorAll("#table-row1")
const displayTable = document.querySelector("#myTable1")

function myFunction(e) {

  var input, filter, table, tr, td, i, txtValue;

  input = document.getElementById("form-field-membersearch1");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable1");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > 0) {
        displayTable.classList.remove('hidden')
        tr[i].style.display = "";
      } else {
        textArea.innerText = ''
        tr[i].style.display = "none";
      }
    }
  }
}


TableRow.forEach(item => {
item.addEventListener('click', function (event) {
let table = document.querySelector("#myTable1")
let tr = table.getElementsByTagName("tr")
searchInput.value = item.innerText
memberList.forEach(items => {
    if (items.username === item.innerText){
        textArea.innerText = JSON.stringify(items)
    }
})
for (let i = 0; i < tr.length; i++) {
  tr[i].style.display = "none";
}


});
});

searchInput.addEventListener('keyup',myFunction)