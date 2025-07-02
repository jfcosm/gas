document.addEventListener("DOMContentLoaded", function () {
  const regionSelect = document.getElementById("region") || document.getElementById("id_region");
  const comunaSelect = document.getElementById("comuna") || document.getElementById("id_comuna");

  if (!regionSelect || !comunaSelect) {
    console.warn("No se encontraron los campos región o comuna.");
    return;
  }

  fetch("/static/core/data/comunas_regiones.json")
    .then((response) => response.json())
    .then((data) => {
      const regiones = data.regiones;

      regionSelect.addEventListener("change", function () {
        const regionSeleccionada = this.value;
        const regionData = regiones.find((r) => r.region === regionSeleccionada);

        comunaSelect.innerHTML = "";

        if (regionData) {
          regionData.comunas.forEach((comuna) => {
            const option = document.createElement("option");
            option.value = comuna;
            option.textContent = comuna;
            comunaSelect.appendChild(option);
          });
        } else {
          const option = document.createElement("option");
          option.textContent = "Seleccione una región válida";
          comunaSelect.appendChild(option);
        }
      });
    })
    .catch((error) => {
      console.error("Error al cargar comunas_regiones.json:", error);
    });
});
