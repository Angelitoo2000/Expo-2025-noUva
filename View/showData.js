import getData from "../API/getData.js";

async function showData() {
    const apiData = await getData();
    const div = document.getElementById("container");
    if (apiData) { 
        apiData.forEach(a => {
            const pe = document.createElement("p");
            pe.innerHTML = `Nombre: ${a.nombre} <br> Descripción: ${a.descripcion}`;
            div.appendChild(pe);
        });
    } else {
        div.innerHTML = "<p>Error: No se pudieron obtener los datos de la API.</p>";
    }
}
export default showData;