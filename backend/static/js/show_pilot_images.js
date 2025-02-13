document.addEventListener('DOMContentLoaded', function() {
    window.showImages = function(itemId) {
        fetch(`/get-images/${itemId}`)
            .then(response => response.json())
            .then(item => {
                const gallery = document.getElementById('imageGallery');
                gallery.innerHTML = '';
                
                if (item.images.produto_imgs) {
                    item.images.produto_imgs.forEach(imageBase64 => {
                        const img = document.createElement('img');
                        img.src = `data:image/jpeg;base64,${imageBase64}`;
                        img.style.maxWidth = '50%';
                        gallery.appendChild(img);
                    });
                }

                if (item.images.trajeto_imgs) {
                    item.images.trajeto_imgs.forEach(imageBase64 => {
                        const img = document.createElement('img');
                        img.src = `data:image/jpeg;base64,${imageBase64}`;
                        img.style.maxWidth = '50%';
                        gallery.appendChild(img);
                    });
                }

                if (item.images.cond_atm_imgs) {
                    item.images.cond_atm_imgs.forEach(imageBase64 => {
                        const img = document.createElement('img');
                        img.src = `data:image/jpeg;base64,${imageBase64}`;
                        img.style.maxWidth = '50%';
                        gallery.appendChild(img);
                    });
                }

                if (item.images.farm_imgs) {
                    item.images.farm_imgs.forEach(imageBase64 => {
                        const img = document.createElement('img');
                        img.src = `data:image/jpeg;base64,${imageBase64}`;
                        img.style.maxWidth = '50%';
                        gallery.appendChild(img);
                    });
                }
                
                document.getElementById('imageModal').style.display = 'block';
            })
            .catch(error => console.error('Error fetching images:', error));
    };
    
    const gallery = document.getElementById('imageGallery');
    console.log("gal lengh", gallery.children.length)
    if (gallery.children.length == 0) {
        gallery.innerHTML = 'Não há imagens.';
    }

    window.hideImages = function() {
        document.getElementById('imageModal').style.display = 'none';
    };

});