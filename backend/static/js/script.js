document.addEventListener('DOMContentLoaded', function() {
    //error and success messages
    const closeButton = document.querySelector('.close');
    const messageElement = document.querySelector('.message');

    if (closeButton){
        closeButton.addEventListener('click', function() {
            messageElement.style.display = 'none';
        });
    }

    //menu on mobile
    const menuOverflow = document.querySelector('.menu-overflow');
    const nav = document.querySelector('.nav');
    const html = document.querySelector('body');

    if (menuOverflow && window.innerWidth < 900) {
        menuOverflow.addEventListener('click', function() {
            
            if (nav.style.display === 'none' || nav.style.display === '') {
                nav.style.display = 'flex';
                html.style.overflowY = 'hidden';
            } else {
                nav.style.display = 'none';
                html.style.overflowY = 'visible';
            }
        });
    } 

    // menu
    const menu = document.querySelectorAll('.menu > li');
   
    menu.forEach(menuItem => {
        menuItem.addEventListener('click', function() {
            
            event.stopPropagation();
            //add bg color when clicke
            menuItem.style.backgroundColor = 'rgba(255, 0, 0, .25)';
            if (window.getComputedStyle(menuItem).backgroundColor == 'rgba(0, 0, 0, .0)') {
                menuItem.style.backgroundColor = 'rgba(0, 0, 0, .25)';
            } else {
                menuItem.style.backgroundColor = 'rgba(0, 0, 0, .0)';
            }
            // menuItem.style.backgroundColor = '#f1f1f1';
            // Get the submenu of the clicked menu item
            const submenu = menuItem.querySelector('.submenu');

            if (submenu) {
                // Check if the submenu is currently displayed
                const isVisible = submenu.style.maxHeight && submenu.style.maxHeight !== '0px';
        
                // Hide all other submenus
                document.querySelectorAll('.submenu').forEach(s => {
                  if (s !== submenu) {
                    s.style.maxHeight = '0px';
                  }
                });

                // Toggle the clicked submenu
                submenu.style.maxHeight = isVisible ? '0px' : '500px';
            }
        })
    });
    
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default link behavior
    
            // Remove active class from all items
            document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));

            this.classList.add('active');
            
        });
    });

});