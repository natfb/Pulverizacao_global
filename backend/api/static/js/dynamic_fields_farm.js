document.addEventListener('DOMContentLoaded', function() {
    let id = document.querySelector('[name="id_farm"]');
    let id_fk = document.querySelector('#farm');

    if ("{{ idt }}" ) {
        const encodedPk = encodeURIComponent(id_fk.value);
        
        fetch(`/fetch-data-farm/${encodedPk}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            for (const [key, value] of Object.entries(data)) {
                const input = document.querySelector(`[name=${key}]`);
                if (input) input.value = value;
            }
        })
        .catch(error => console.error('Error fetching data:', error)); 
    }

    if (id) {
        id.addEventListener('input', function() {
            const encodedPk = encodeURIComponent(id.value);
            if (id.value.length > 3) { //mudar para tamanho do codigo quando mandarem
                fetch(`/fetch-data-farm/${encodedPk}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                        console.log('id')
                    }
                    return response.json();
                })
                .then(data => {
                    for (const [key, value] of Object.entries(data)) {
                        const input = document.querySelector(`[name=${key}]`);
                        if (input) input.value = value;
                    }
                })
                .catch(error => console.error('Error fetching data:', error));
            }
        });
    }
});