import getData from "../API/getData.js";

async function showData() {
    const apiData = await getData();
    const div = document.getElementById("container");
    if (apiData) { // Asegúrate de que los datos no son nulos
        apiData.forEach(a => {
            const pe = document.createElement("p");
            // Aquí, los datos que vienen de la API de Flask se llaman 'nombre' y 'descripcion'
            pe.innerHTML = `Nombre: ${a.nombre} <br> Descripción: ${a.descripcion}`;
            div.appendChild(pe);
        });
    } else {
        div.innerHTML = "<p>Error: No se pudieron obtener los datos de la API.</p>";
    }
}
export default showData;