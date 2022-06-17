var xxx = document.getElementById("files");
var file = document.getElementById("filename");
var upload = document.getElementById("upload");
var submit = document.getElementById("submit");

xxx.addEventListener("change", function () {
  file.innerText = this.value.replace(/.*[\/\\]/, "");
});

upload.addEventListener("click", function (e) {
  //   e.preventDefault();
  submit.click();
});
