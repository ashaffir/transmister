// scripts.js
function runButtonClicked() {
    const spinner = document.getElementById('spinner');
    spinner.classList.remove('hidden');

    someFunction().then(() => {
        spinner.classList.add('hidden');
    });
}

async function someFunction() {
    const url = 'https://api.example.com/your-endpoint';

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        // Process the data as needed
    } catch (error) {
        console.error('Error:', error);
    }
}
