import url from "./url.js";

async function getData() {
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`¡Error! El servidor respondió con el código: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Hubo un problema al obtener los datos:", error);
    }
}

export default getData;