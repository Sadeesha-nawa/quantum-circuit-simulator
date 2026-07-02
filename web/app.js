const runButton = document.getElementById("runButton");
const statusBox = document.getElementById("status");
const shotsInput = document.getElementById("shots");

const circuitOutput = document.getElementById("circuitOutput");
const stateOutput = document.getElementById("stateOutput");
const probabilityOutput = document.getElementById("probabilityOutput");
const measurementOutput = document.getElementById("measurementOutput");

let pyodide = null;

async function loadPythonFile(path, filename) {
    const response = await fetch(path);

    if (!response.ok) {
        throw new Error(`Could not load ${path}`);
    }

    const code = await response.text();
    pyodide.FS.writeFile(filename, code);
}

async function initializePyodide() {
    try {
        statusBox.textContent = "Loading Pyodide...";
        pyodide = await loadPyodide();

        statusBox.textContent = "Loading NumPy...";
        await pyodide.loadPackage("numpy");

        statusBox.textContent = "Loading simulator files...";
        await loadPythonFile("python/quantum_sim.py", "quantum_sim.py");
        await loadPythonFile("python/circuit.py", "circuit.py");
        await loadPythonFile("python/web_runner.py", "web_runner.py");

        statusBox.textContent = "Importing simulator...";
        await pyodide.runPythonAsync(`
            from web_runner import run_bell_demo, run_circuit
        `);

        statusBox.textContent = "Ready.";
        runButton.textContent = "Run Bell State Demo";
        runButton.disabled = false;
    } catch (error) {
        console.error(error);
        statusBox.textContent = "Error loading simulator. Check the browser console.";
    }
}

function displayResult(result) {
    circuitOutput.textContent = result.summary;
    stateOutput.textContent = result.state;
    probabilityOutput.textContent = JSON.stringify(result.probabilities, null, 2);
    measurementOutput.textContent = JSON.stringify(result.measurement, null, 2);
}

runButton.addEventListener("click", () => {
    const shots = Number.parseInt(shotsInput.value, 10) || 1000;

    const operations = [
        { gate: "H", target: 0 },
        { gate: "CNOT", control: 0, target: 1 }
    ];

    pyodide.globals.set("num_qubits", 2);
    pyodide.globals.set("operations_json", JSON.stringify(operations));
    pyodide.globals.set("shots", shots);

    const resultJson = pyodide.runPython("run_circuit(num_qubits, operations_json, shots)");
    const result = JSON.parse(resultJson);

    displayResult(result);
});

initializePyodide();