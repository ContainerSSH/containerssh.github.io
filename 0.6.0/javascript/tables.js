app.document$.subscribe(function() {
  let tables = document.querySelectorAll("article table");
  tables.forEach(function(table) {
    new Tablesort(table)
  })
})
