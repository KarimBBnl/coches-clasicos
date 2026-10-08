// Configure this with the independent API Gateway endpoint for this project.
const API_CONFIG = { contactEndpoint: '' };

document.addEventListener('DOMContentLoaded', () => {
  const selectedVehicleLabel = document.getElementById('selected-vehicle-label');
  const vehicleForm = document.getElementById('vehicle-inquiry-form');
  const nameInput = document.getElementById('name');
  const emailInput = document.getElementById('email');
  const phoneInput = document.getElementById('phone');
  const messageInput = document.getElementById('message');
  const formError = document.getElementById('form-error');
  const formStatus = document.getElementById('form-status');
  const submitButton = vehicleForm?.querySelector('button[type="submit"]');
  const contactSection = document.getElementById('contacto');
  const carButtons = document.querySelectorAll('.car-action');

  if (!selectedVehicleLabel || !vehicleForm || !nameInput || !emailInput ||
      !phoneInput || !messageInput || !formError || !formStatus ||
      !submitButton || !contactSection) {
    console.error('No se pudo inicializar la página: faltan elementos requeridos.');
    return;
  }

  let selectedVehicle = '';

  function updateSelectedVehicle(nextVehicle) {
    selectedVehicle = nextVehicle;
    selectedVehicleLabel.textContent = selectedVehicle || 'Sin selección';
  }

  function showStatus(message, type = 'default') {
    formStatus.textContent = message;
    formStatus.className = 'status-message';
    if (type !== 'default') formStatus.classList.add(`is-${type}`);
  }

  carButtons.forEach((button) => {
    button.addEventListener('click', () => {
      updateSelectedVehicle(button.dataset.vehicle || '');
      contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      messageInput.focus();
      showStatus('Vehículo seleccionado. Completa la consulta para solicitar información.', 'warning');
    });
  });

  vehicleForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    formError.textContent = '';

    if (!vehicleForm.reportValidity()) return;

    if (!API_CONFIG.contactEndpoint) {
      showStatus('El formulario está preparado, pero la API propia del proyecto aún no está configurada.', 'warning');
      formError.textContent = 'La consulta no se ha enviado. Primero hay que desplegar y configurar el backend de Car Classic San Valero.';
      return;
    }

    const message = selectedVehicle
      ? `Vehículo de interés: ${selectedVehicle}\n\n${messageInput.value.trim()}`
      : messageInput.value.trim();

    showStatus('Enviando consulta…', 'warning');
    submitButton.disabled = true;

    try {
      const response = await fetch(API_CONFIG.contactEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: nameInput.value.trim(),
          email: emailInput.value.trim(),
          phone: phoneInput.value.trim(),
          message
        })
      });
      const result = await response.json();

      if (!response.ok || result.success === false) {
        throw new Error(result.error || result.message || `La API respondió con HTTP ${response.status}.`);
      }

      showStatus(result.message || 'Consulta enviada correctamente.', 'success');
      vehicleForm.reset();
      updateSelectedVehicle('');
    } catch (error) {
      console.error('No se pudo enviar la consulta:', error);
      showStatus(`No se pudo enviar la consulta: ${error.message}`, 'error');
    } finally {
      submitButton.disabled = false;
    }
  });
});
