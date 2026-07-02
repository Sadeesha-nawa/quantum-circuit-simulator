const runButton = document.getElementById("runButton");
const addGateButton = document.getElementById("addGateButton");
const resetButton = document.getElementById("resetButton");

const statusBox = document.getElementById("status");
const shotsInput = document.getElementById("shots");

const numQubitsSelect = document.getElementById("numQubits");
const gateSelect = document.getElementById("gateSelect");
const targetQubitSelect = document.getElementById("targetQubit");
const controlQubitSelect = document.getElementById("controlQubit");

const operationList = document.getElementById("operationList");

const circuitOutput = document.getElementById("circuitOutput");
const stateOutput = document.getElementById("stateOutput");
const probabilityOutput = document.getElementById("probabilityOutput");
const measurementOutput = document.getElementById("measurementOutput");

let pyodide = null;
let operations = [];


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
        pyodide = await loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/"
        });

        statusBox.textContent = "Loading NumPy...";
        await pyodide.loadPackage("numpy");

        statusBox.textContent = "Loading simulator files...";
        await loadPythonFile("python/quantum_sim.py", "quantum_sim.py");
        await loadPythonFile("python/circuit.py", "circuit.py");
        await loadPythonFile("python/web_runner.py", "web_runner.py");

        statusBox.textContent = "Importing simulator...";
        await pyodide.runPythonAsync(`
            from web_runner import run_circuit
        `);

        statusBox.textContent = "Ready.";
        runButton.textContent = "Run Circuit";

        addGateButton.disabled = false;
        runButton.disabled = false;
        resetButton.disabled = false;

        updateQubitOptions();
        updateOperationList();
    } catch (error) {
        console.error(error);
        statusBox.textContent = "Error loading simulator. Check the browser console.";
    }
}


function updateQubitOptions() {
    const numQubits = Number.parseInt(numQubitsSelect.value, 10);

    targetQubitSelect.innerHTML = "";
    controlQubitSelect.innerHTML = "";

    for (let i = 0; i < numQubits; i++) {
        const targetOption = document.createElement("option");
        targetOption.value = i;
        targetOption.textContent = `Qubit ${i}`;
        targetQubitSelect.appendChild(targetOption);

        const controlOption = document.createElement("option");
        controlOption.value = i;
        controlOption.textContent = `Qubit ${i}`;
        controlQubitSelect.appendChild(controlOption);
    }

    if (numQubits > 1) {
        controlQubitSelect.value = "0";
        targetQubitSelect.value = "1";
    }
}


function addGate() {
    const gate = gateSelect.value;
    const target = Number.parseInt(targetQubitSelect.value, 10);
    const control = Number.parseInt(controlQubitSelect.value, 10);

    if (gate === "CNOT") {
        if (control === target) {
            statusBox.textContent = "For CNOT, control and target must be different.";
            return;
        }

        operations.push({
            gate: gate,
            control: control,
            target: target
        });
    } else {
        operations.push({
            gate: gate,
            target: target
        });
    }

    statusBox.textContent = "Gate added.";
    updateOperationList();
}


function updateOperationList() {
    if (operations.length === 0) {
        operationList.textContent = "No gates added yet.";
        return;
    }

    const lines = operations.map((operation, index) => {
        if (operation.gate === "CNOT") {
            return `${index + 1}. CNOT control=${operation.control} target=${operation.target}`;
        }

        return `${index + 1}. ${operation.gate} on qubit ${operation.target}`;
    });

    operationList.textContent = lines.join("\n");
}


function basisLabels(numQubits) {
    const labels = [];
    const numStates = 2 ** numQubits;

    for (let i = 0; i < numStates; i++) {
        labels.push(i.toString(2).padStart(numQubits, "0"));
    }

    return labels;
}


function formatNumber(value) {
    return Number(value)
        .toFixed(6)
        .replace(/\.?0+$/, "");
}


function formatProbabilities(probabilities) {
    const numQubits = Math.round(Math.log2(probabilities.length));
    const labels = basisLabels(numQubits);

    return probabilities
        .map((probability, index) => {
            return `|${labels[index]}>: ${formatNumber(probability)}`;
        })
        .join("\n");
}


function formatMeasurement(measurement, probabilities) {
    const numQubits = Math.round(Math.log2(probabilities.length));
    const labels = basisLabels(numQubits);

    return labels
        .map((label) => {
            const count = measurement[label] ?? 0;
            return `|${label}>: ${count}`;
        })
        .join("\n");
}


function displayResult(result) {
    circuitOutput.textContent = result.summary;
    stateOutput.textContent = result.state;
    probabilityOutput.textContent = formatProbabilities(result.probabilities);
    measurementOutput.textContent = formatMeasurement(result.measurement, result.probabilities);
}


function runCircuit() {
    const numQubits = Number.parseInt(numQubitsSelect.value, 10);
    const shots = Number.parseInt(shotsInput.value, 10) || 1000;

    pyodide.globals.set("num_qubits", numQubits);
    pyodide.globals.set("operations_json", JSON.stringify(operations));
    pyodide.globals.set("shots", shots);

    const resultJson = pyodide.runPython("run_circuit(num_qubits, operations_json, shots)");
    const result = JSON.parse(resultJson);

    displayResult(result);
    statusBox.textContent = "Circuit ran successfully.";
}


function resetCircuit() {
    operations = [];
    updateOperationList();

    circuitOutput.textContent = "Waiting for simulator...";
    stateOutput.textContent = "Waiting for simulator...";
    probabilityOutput.textContent = "Waiting for simulator...";
    measurementOutput.textContent = "Waiting for simulator...";

    statusBox.textContent = "Circuit reset.";
}


numQubitsSelect.addEventListener("change", () => {
    operations = [];
    updateQubitOptions();
    updateOperationList();
    statusBox.textContent = "Number of qubits changed. Circuit reset.";
});

addGateButton.addEventListener("click", addGate);
runButton.addEventListener("click", runCircuit);
resetButton.addEventListener("click", resetCircuit);

initializePyodide();