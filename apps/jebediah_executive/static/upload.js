(function () {
  "use strict";

  var questionForm = document.querySelector("[data-question-form]");
  if (questionForm) {
    var questionButton = questionForm.querySelector(".question-submit");
    var questionStatus = questionForm.querySelector(".question-processing-status");
    questionForm.addEventListener("submit", function () {
      questionForm.classList.add("is-submitting");
      questionForm.setAttribute("aria-busy", "true");
      questionButton.disabled = true;
      questionStatus.textContent = "Reviewing approved evidence and preparing a cited answer…";
    });
    window.addEventListener("pageshow", function () {
      questionForm.classList.remove("is-submitting");
      questionForm.removeAttribute("aria-busy");
      questionButton.disabled = false;
    });
  }

  var form = document.querySelector("[data-upload-form]");
  if (!form) {
    return;
  }

  var fileInput = document.getElementById("document_file");
  var dropzone = document.getElementById("upload-dropzone");
  var queueElement = document.getElementById("upload-queue");
  var summary = document.getElementById("upload-summary");
  var errors = document.getElementById("upload-errors");
  var submitButton = document.getElementById("upload-submit");
  var sourceRecordInput = document.getElementById("source_record_id");
  var maxFileSize = Number(form.dataset.maxFileSize || "1000000");
  var allowedTypes = {
    pdf: new Set(["application/pdf", "application/octet-stream", ""]),
    docx: new Set([
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/octet-stream",
      "",
    ]),
    xlsx: new Set([
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "application/octet-stream",
      "",
    ]),
    pptx: new Set([
      "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      "application/octet-stream",
      "",
    ]),
    csv: new Set([
      "text/csv",
      "application/csv",
      "application/vnd.ms-excel",
      "text/plain",
      "application/octet-stream",
      "",
    ]),
    txt: new Set(["text/plain", "application/octet-stream", ""]),
    md: new Set(["text/markdown", "text/x-markdown", "text/plain", "application/octet-stream", ""]),
    markdown: new Set(["text/markdown", "text/x-markdown", "text/plain", "application/octet-stream", ""]),
  };
  var items = [];
  var hashes = new Map();
  var nextId = 1;
  var submitting = false;

  form.classList.add("upload-enhanced");
  // The enhanced uploader owns file validation and submission from its in-memory queue.
  // Keep the native required constraint only for the no-JavaScript fallback; otherwise
  // clearing the picker after queueing a file prevents the submit event from firing.
  fileInput.removeAttribute("required");
  dropzone.hidden = false;

  function extensionOf(fileName) {
    var parts = fileName.toLowerCase().split(".");
    return parts.length > 1 ? parts.pop() : "";
  }

  function formatSize(bytes) {
    if (bytes < 1000) {
      return bytes + " bytes";
    }
    if (bytes < 1000000) {
      return (bytes / 1000).toFixed(1) + " KB";
    }
    return (bytes / 1000000).toFixed(2) + " MB";
  }

  function mediaTypeFor(file) {
    var extension = extensionOf(file.name);
    if (extension === "pdf") {
      return "application/pdf";
    }
    if (extension === "docx") {
      return "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
    }
    if (extension === "xlsx") {
      return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    }
    if (extension === "pptx") {
      return "application/vnd.openxmlformats-officedocument.presentationml.presentation";
    }
    if (extension === "csv") {
      return "text/csv";
    }
    if (extension === "txt") {
      return "text/plain";
    }
    if (["md", "markdown"].includes(extension)) {
      return "text/markdown";
    }
    return file.type || "application/octet-stream";
  }

  function validateFile(file) {
    var extension = extensionOf(file.name);
    if (!allowedTypes[extension] || !allowedTypes[extension].has(file.type || "")) {
      return "Unsupported file type. Choose PDF, DOCX, XLSX, PPTX, CSV, TXT, or Markdown.";
    }
    if (file.size === 0) {
      return "The file is empty and cannot enter governed admission.";
    }
    if (file.size > maxFileSize) {
      return "The file exceeds the 1 MB admission limit.";
    }
    return "";
  }

  function showErrors(messages) {
    if (!messages.length) {
      errors.hidden = true;
      errors.replaceChildren();
      return;
    }
    var heading = document.createElement("p");
    heading.className = "upload-errors-heading";
    heading.textContent = messages.length === 1 ? "Upload validation failed" : "Some files could not be queued";
    var list = document.createElement("ul");
    messages.forEach(function (message) {
      var entry = document.createElement("li");
      entry.textContent = message;
      list.appendChild(entry);
    });
    errors.replaceChildren(heading, list);
    errors.hidden = false;
    errors.focus();
  }

  function updateSummary() {
    var ready = items.filter(function (item) { return item.state === "ready"; }).length;
    var active = items.filter(function (item) {
      return ["validating", "uploading", "submitting"].includes(item.state);
    }).length;
    var complete = items.filter(function (item) { return item.state === "complete"; }).length;
    var failed = items.filter(function (item) { return item.state === "failed"; }).length;
    if (!items.length) {
      summary.textContent = "No files queued.";
      return;
    }
    summary.textContent = [
      items.length + (items.length === 1 ? " file" : " files"),
      ready + " ready",
      active + " processing",
      complete + " admitted",
      failed + " failed",
    ].join(" · ");
  }

  function metadataRow(label, value, className) {
    var term = document.createElement("dt");
    term.textContent = label;
    var description = document.createElement("dd");
    description.textContent = value;
    if (className) {
      description.className = className;
    }
    return [term, description];
  }

  function createQueueItem(file) {
    var item = {
      id: nextId++,
      file: file,
      digest: "",
      state: "validating",
      response: null,
    };
    var row = document.createElement("li");
    row.className = "upload-item is-validating";
    row.dataset.uploadId = String(item.id);

    var header = document.createElement("div");
    header.className = "upload-item-header";
    var title = document.createElement("h4");
    title.textContent = file.name;
    var remove = document.createElement("button");
    remove.type = "button";
    remove.className = "upload-remove";
    remove.textContent = "Remove";
    remove.setAttribute("aria-label", "Remove " + file.name + " from upload queue");
    remove.addEventListener("click", function () {
      if (submitting || !["ready", "failed"].includes(item.state)) {
        return;
      }
      if (item.digest && hashes.get(item.digest) === item) {
        hashes.delete(item.digest);
      }
      items = items.filter(function (candidate) { return candidate !== item; });
      row.remove();
      updateSummary();
    });
    header.append(title, remove);

    var status = document.createElement("p");
    status.className = "upload-status";
    status.setAttribute("role", "status");
    status.textContent = "Validating...";

    var progress = document.createElement("progress");
    progress.max = 100;
    progress.value = 0;
    progress.setAttribute("aria-label", "Upload progress for " + file.name);
    progress.hidden = true;

    var metadata = document.createElement("dl");
    metadata.className = "upload-metadata";
    var sizeRow = metadataRow("Size", formatSize(file.size));
    var hashRow = metadataRow("SHA-256", "Calculating...", "upload-hash");
    var stateRow = metadataRow("Admission state", "Validating", "upload-state");
    var timeRow = metadataRow("Submitted", "Not submitted", "upload-time");
    metadata.append.apply(metadata, sizeRow.concat(hashRow, stateRow, timeRow));

    row.append(header, status, progress, metadata);
    queueElement.appendChild(row);
    item.elements = {
      row: row,
      status: status,
      progress: progress,
      hash: hashRow[1],
      admissionState: stateRow[1],
      submittedAt: timeRow[1],
      remove: remove,
    };
    items.push(item);
    updateSummary();
    return item;
  }

  function setItemState(item, state, statusText, admissionText) {
    item.state = state;
    item.elements.row.className = "upload-item is-" + state;
    item.elements.status.textContent = statusText;
    item.elements.admissionState.textContent = admissionText || statusText;
    item.elements.remove.disabled = submitting || !["ready", "failed"].includes(state);
    updateSummary();
  }

  async function digestFile(file) {
    var buffer = await file.arrayBuffer();
    var digest = await window.crypto.subtle.digest("SHA-256", buffer);
    return Array.from(new Uint8Array(digest)).map(function (byte) {
      return byte.toString(16).padStart(2, "0");
    }).join("");
  }

  async function prepareItem(item) {
    try {
      item.digest = await digestFile(item.file);
      item.elements.hash.textContent = item.digest;
      if (hashes.has(item.digest)) {
        setItemState(
          item,
          "failed",
          "Upload failed: duplicate file",
          "Duplicate content was not submitted"
        );
        showErrors([item.file.name + ": Duplicate content is already queued."]);
        return;
      }
      hashes.set(item.digest, item);
      setItemState(item, "ready", "Ready to submit", "Not submitted");
    } catch (_error) {
      setItemState(item, "failed", "Upload failed", "Hash validation failed");
      showErrors([item.file.name + ": The browser could not validate this file."]);
    }
  }

  async function addFiles(fileList) {
    var validationErrors = [];
    var accepted = [];
    Array.from(fileList).forEach(function (file) {
      var message = validateFile(file);
      if (message) {
        validationErrors.push(file.name + ": " + message);
      } else {
        accepted.push(file);
      }
    });
    showErrors(validationErrors);
    for (var index = 0; index < accepted.length; index += 1) {
      await prepareItem(createQueueItem(accepted[index]));
    }
  }

  function uploadItem(item, sourceRecordId) {
    return new Promise(function (resolve, reject) {
      var request = new XMLHttpRequest();
      var payload = new FormData();
      payload.append("source_record_id", sourceRecordId);
      var csrf = form.querySelector("input[name='csrf_token']");
      if (csrf && csrf.value) {
        payload.append("csrf_token", csrf.value);
      }
      payload.append("document_file", item.file, item.file.name);

      request.open("POST", form.action);
      request.setRequestHeader("Accept", "application/json");
      request.upload.addEventListener("progress", function (event) {
        if (!event.lengthComputable) {
          return;
        }
        var percent = Math.max(1, Math.min(100, Math.round((event.loaded / event.total) * 100)));
        item.elements.progress.value = percent;
        item.elements.status.textContent = "Uploading... " + percent + "%";
      });
      request.upload.addEventListener("load", function () {
        setItemState(item, "submitting", "Submitting...", "Governed admission is evaluating the file");
      });
      request.addEventListener("load", function () {
        var response;
        try {
          response = JSON.parse(request.responseText || "{}");
        } catch (_error) {
          reject(new Error("The admission service returned an unreadable response."));
          return;
        }
        if (request.status < 200 || request.status >= 300 || response.ok !== true) {
          reject(new Error(response.error || "The governed admission service rejected this file."));
          return;
        }
        resolve(response);
      });
      request.addEventListener("error", function () {
        reject(new Error("The upload connection failed. Check the runtime and try again."));
      });
      request.addEventListener("abort", function () {
        reject(new Error("The upload was interrupted before admission completed."));
      });
      item.elements.progress.hidden = false;
      setItemState(item, "uploading", "Uploading... 0%", "Uploading");
      request.send(payload);
    });
  }

  async function submitQueue(event) {
    event.preventDefault();
    if (submitting) {
      return;
    }
    var sourceRecordId = sourceRecordInput.value.trim();
    var pending = items.filter(function (item) { return item.state === "ready"; });
    if (!sourceRecordId) {
      showErrors(["Enter a source record ID before submitting documents."]);
      sourceRecordInput.focus();
      return;
    }
    if (!pending.length) {
      showErrors(["Choose at least one supported business document."]);
      dropzone.focus();
      return;
    }

    showErrors([]);
    submitting = true;
    submitButton.disabled = true;
    fileInput.disabled = true;
    dropzone.disabled = true;
    items.forEach(function (item) { item.elements.remove.disabled = true; });

    for (var index = 0; index < pending.length; index += 1) {
      var item = pending[index];
      try {
        var response = await uploadItem(item, sourceRecordId);
        item.response = response;
        item.elements.progress.value = 100;
        item.elements.hash.textContent = response.sha256 || item.digest;
        item.elements.submittedAt.textContent = response.submitted_at
          ? new Date(response.submitted_at).toLocaleString()
          : new Date().toLocaleString();
        setItemState(
          item,
          "complete",
          "Admission complete",
          response.admission_state === "review_pending"
            ? "Awaiting approval"
            : String(response.admission_state || "Admission complete")
        );
      } catch (error) {
        item.elements.progress.hidden = true;
        setItemState(item, "failed", "Upload failed", "Admission failed");
        showErrors([item.file.name + ": " + error.message]);
      }
    }

    submitting = false;
    submitButton.disabled = false;
    fileInput.disabled = false;
    dropzone.disabled = false;
    items.forEach(function (item) {
      item.elements.remove.disabled = !["ready", "failed"].includes(item.state);
    });
    updateSummary();
  }

  fileInput.addEventListener("change", function () {
    addFiles(fileInput.files);
    fileInput.value = "";
  });
  dropzone.addEventListener("click", function () {
    fileInput.click();
  });
  ["dragenter", "dragover"].forEach(function (eventName) {
    dropzone.addEventListener(eventName, function (event) {
      event.preventDefault();
      if (!dropzone.disabled) {
        dropzone.classList.add("is-dragover");
      }
    });
  });
  ["dragleave", "drop"].forEach(function (eventName) {
    dropzone.addEventListener(eventName, function (event) {
      event.preventDefault();
      dropzone.classList.remove("is-dragover");
    });
  });
  dropzone.addEventListener("drop", function (event) {
    if (!dropzone.disabled && event.dataTransfer) {
      addFiles(event.dataTransfer.files);
    }
  });
  form.addEventListener("submit", submitQueue);
}());