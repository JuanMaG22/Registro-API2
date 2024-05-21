const agregarMascotaForm = document.getElementById('agregarMascotaForm');

agregarMascotaForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const mascotaData = {
        nombre: document.getElementById('nombre').value,
        especie: document.getElementById('especie').value,
        edad: parseInt(document.getElementById('edad').value),
        descripcion: document.getElementById('descripcion').value
    };

    fetch('/mascotas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(mascotaData)
    })
        .then(response => response.json())
        .then(data => {
            // Mostrar mensaje de éxito o redireccionar
            console.log('Mascota agregada:', data);
        });
});

// Abrir modal para agregar mascota
const abrirAgregarModalBtn = document.getElementById('abrirAgregarModal');
const agregarMascotaModal = document.getElementById('agregarMascotaModal');

abrirAgregarModalBtn.addEventListener('click', () => {
    agregarMascotaModal.classList.add('active');
});

// Cerrar modal para agregar mascota (puedes usar un botón o hacer clic fuera del modal)
agregarMascotaModal.addEventListener('click', (event) => {
    if (event.target === agregarMascotaModal) {
        agregarMascotaModal.classList.remove('active');
    }
});