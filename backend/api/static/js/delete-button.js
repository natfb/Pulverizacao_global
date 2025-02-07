document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("delete-btn").addEventListener("click", function(event) {
        if (!confirm("Tem certeza que deseja deletar este item?")) {
            event.preventDefault();  // Stop form submission if user cancels
        }
    });

    buttonDelet = document.getElementById("delete-btn");
    if (window.location.pathname.includes('/edit/')) { 
        buttonDelet.style.display = "block";
    } else if (window.location.pathname.includes('/edit-guia-piloto/')) {
        buttonDelet.style.display = "block";
    } else {
        buttonDelet.style.display = "none";
    }

    //guia aplic piot
    // if (window.location.pathname.includes('/edit-guia-piloto/')) { 
    //     buttonDelet.style.display = "block";
    // } else {
    //     buttonDelet.style.display = "none";
    // }

    //ediatr talhoes e fazendas
    document.getElementById("delete-btn2").addEventListener("click", function(event) {
        if (!confirm("Tem certeza que deseja deletar este item?")) {
            event.preventDefault();  // Stop form submission if user cancels
        }
    });

    buttonDelet2 = document.getElementById("delete-btn2");
    if (window.location.pathname.includes('/edit-talhao/')) {
        console.log("edit tal")
        
        buttonDelet2.style.display = "block";
    } else {
        buttonDelet2.style.display = "none";
    }

    
});