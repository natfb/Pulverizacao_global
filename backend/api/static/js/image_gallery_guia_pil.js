document.addEventListener("DOMContentLoaded", function() {
    const btnShowForm = document.querySelectorAll(".btn-show-form");

    btnShowForm.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const guiaPilotoForm = document.getElementById(targetId);

            if (guiaPilotoForm.classList.contains("show")) {
                guiaPilotoForm.classList.remove("show");
                button.textContent = 'Preencher';
            } else {
                guiaPilotoForm.classList.add("show");
                button.textContent = 'Esconder formulário';
            }
        });
    });
    
    const currentPath = window.location.pathname;
    if (currentPath.includes('/edit-guia-piloto/')) {
        const idMatch = currentPath.match(/\/edit-guia-piloto\/(\d+)(\/)?/);
        const btnShowForm = document.querySelector(`button[data-target="form-${idMatch[1]}"`);
        const targetId = btnShowForm.getAttribute('data-target');
        const guiaPilotoForm = document.getElementById(targetId);
        
        guiaPilotoForm.classList.add("show");
        btnShowForm.textContent = 'Esconder formulário';
    }

//upload de fotos

let fileArray1 = []; 
let fileArray2 = []; 
let fileArray3 = []; 
let fileArray4 = []; 

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(dropArea) {
    dropArea.classList.add('drag-over');
}

function unhighlight(dropArea) {
    dropArea.classList.remove('drag-over');
}

function handleFiles(files, galleryId, fileArray, inputElem) {
    let gallery = document.getElementById(galleryId);
    
    Array.from(files).forEach(file => {
        fileArray.push(file); 

        let imgContainer = document.createElement("div");
        imgContainer.classList.add("img-container");

        let img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.height = 100;
        img.style.margin = "5px";

        let removeButton = document.createElement("span");
        removeButton.classList.add("remove-btn");
        removeButton.innerHTML = "&times;";

        removeButton.onclick = function() {
            const index = fileArray.indexOf(file);
            if (index > -1) {
                fileArray.splice(index, 1); 
                updateFileInput(fileArray, inputElem); 
            }
            gallery.removeChild(imgContainer); 
        };

        imgContainer.appendChild(img);
        imgContainer.appendChild(removeButton);
        gallery.appendChild(imgContainer);
    });
    
    updateFileInput(fileArray, inputElem); 
}

function updateFileInput(fileArray, inputElem) {
    const dataTransfer = new DataTransfer();
    fileArray.forEach(file => dataTransfer.items.add(file));
    inputElem.files = dataTransfer.files; // Update input files
}

function setupDropArea(dropAreaId, fileInputId, galleryId, fileArray) {
    const dropArea = document.getElementById(dropAreaId);
    const fileInput = document.getElementById(fileInputId);

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => highlight(dropArea), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => unhighlight(dropArea), false);
    });

    dropArea.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        handleFiles(files, galleryId, fileArray, fileInput);
    });

    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files, galleryId, fileArray, fileInput);
    });
}

// remover imagens existentes na edicao
let imagesToDeleteFarm = [];  

function removeExistingImageFarm(button) {
    const imgContainer = button.parentElement;
    const imageId = imgContainer.getAttribute('data-id');

    if (imageId) {
        imagesToDeleteFarm.push(imageId);
        imgContainer.remove();  
    }

    document.getElementById('images_to_delete_farm').value = imagesToDeleteFarm.join(',');
}

let imagesToDeleteProd = [];  

function removeExistingImageProd(button) {
    const imgContainer = button.parentElement;
    const imageId = imgContainer.getAttribute('data-id');

    if (imageId) {
        imagesToDeleteProd.push(imageId);
        imgContainer.remove();  
    }

    document.getElementById('images_to_delete_prod').value = imagesToDeleteProd.join(',');
}

let imagesToDeleteCond = [];  

function removeExistingImageCond(button) {
    const imgContainer = button.parentElement;
    const imageId = imgContainer.getAttribute('data-id');

    if (imageId) {
        imagesToDeleteCond.push(imageId);
        imgContainer.remove();  
    }

    document.getElementById('images_to_delete_cond').value = imagesToDeleteCond.join(',');
}

let imagesToDeleteTraj = [];  

function removeExistingImageTraj(button) {
    const imgContainer = button.parentElement;
    const imageId = imgContainer.getAttribute('data-id');

    if (imageId) {
        imagesToDeleteTraj.push(imageId);
        imgContainer.remove();  
    }

    document.getElementById('images_to_delete_traj').value = imagesToDeleteTraj.join(',');
}

setupDropArea("drop-area1", "fileElem1", "gallery1", fileArray1);
setupDropArea("drop-area2", "fileElem2", "gallery2", fileArray2);
setupDropArea("drop-area3", "fileElem3", "gallery3", fileArray3);
setupDropArea("drop-area4", "fileElem4", "gallery4", fileArray4);

window.removeExistingImageFarm = removeExistingImageFarm;
window.removeExistingImageProd = removeExistingImageProd;
window.removeExistingImageCond = removeExistingImageCond;
window.removeExistingImageTraj = removeExistingImageTraj;
});