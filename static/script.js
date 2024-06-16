let currentTaskId = null;

// Populate the format dropdown
fetch("/formats")
  .then((response) => response.json())
  .then((data) => {
    const select = document.getElementById("outputFormat");
    data.formats.forEach((format) => {
      const option = document.createElement("option");
      option.value = format;
      option.textContent = format;
      select.appendChild(option);
    });
  });

document.getElementById("imageFile").addEventListener("change", function (e) {
  const fileName = e.target.files[0].name;
  document.getElementById("fileName").textContent = fileName;
});

// Handle form submission
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData();
  const fileInput = document.getElementById("imageFile");
  formData.append("file", fileInput.files[0]);
  formData.append(
    "output_format",
    document.getElementById("outputFormat").value
  );

  document.getElementById("status").textContent = "Uploading and processing...";

  try {
    const response = await fetch("/upload/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    if (response.ok) {
      currentTaskId = result.task_id;
      checkStatus(currentTaskId);
    } else {
      document.getElementById("status").textContent = `Error: ${result.detail}`;
    }
  } catch (error) {
    document.getElementById("status").textContent = `Error: ${error.message}`;
  }
});

document.getElementById("imageFile").addEventListener("change", function (e) {
  const fileName = e.target.files[0].name;
  document.getElementById("fileName").textContent = fileName;
});

// Check conversion status
function checkStatus(taskId) {
  const statusElement = document.getElementById("status");
  const downloadElement = document.getElementById("download");

  function pollStatus() {
    fetch(`/status/${taskId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "completed") {
          statusElement.textContent = "Conversion completed!";
          const filename = `${taskId}.${document
            .getElementById("outputFormat")
            .value.toLowerCase()}`;
          downloadElement.innerHTML = `<a href="/download/${filename}" download>Download Converted Image</a>`;
        } else if (data.status === "failed") {
          statusElement.textContent = `Conversion failed: ${data.error}`;
        } else {
          statusElement.innerHTML =
            "<span>Processing  <i id='spinner' class='fas fa-spinner fa-spin'/></span>";
          setTimeout(pollStatus, 2000); // Check again in 2 seconds
        }
      });
  }

  pollStatus();
}

// Reset UI when selecting a new file
document.getElementById("imageFile").addEventListener("change", () => {
  document.getElementById("status").textContent = "";
  document.getElementById("download").innerHTML = "";
});
