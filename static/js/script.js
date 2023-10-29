  // Get the selection box and input boxes
  const selectionBox = document.getElementById("selectionBox");
  const host = document.getElementById("host");
  const user = document.getElementById("user");
  const pass = document.getElementById("password");
  const db = document.getElementById("database");


  // Add an event listener to the selection box
  selectionBox.addEventListener("change", function () {
      // Hide all input boxes
      host.style.display = "none";
      user.style.display = "none";
      pass.style.display = "none";
      db.style.display  = "none";

      // Show the selected input box
      const selectedOption = selectionBox.value;
      if (selectedOption === "PostgresSQL" || selectedOption === "MySQL") {
        host.style.display = "block";
        user.style.display = "block";
        pass.style.display = "block";
        db.style.display = "block";
      } 
  });