const runButton = document.getElementById("runButton");
const addGateButton = document.getElementById("addGateButton");
const bellExampleButton = document.getElementById("bellExampleButton");
const resetButton = document.getElementById("resetButton");

const statusBox = document.getElementById("status");
const shotsInput = document.getElementById("shots");

const numQubitsSelect = document.getElementById("numQubits");
const gateSelect = document.getElementById("gateSelect");
const targetQubitSelect = document.getElementById("targetQubit");
const controlQubitSelect = document.getElementById("controlQubit");
const controlQubitGroup = document.getElementById("controlQubitGroup");

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
        bellExampleButton.disabled = false;
        runButton.disabled = false;
        resetButton.disabled = false;

        updateQubitOptions();
        updateGateControls();
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

function updateGateControls() {
    const numQubits = Number.parseInt(numQubitsSelect.value, 10);
    const cnotOption = Array.from(gateSelect.options).find((option) => {
        return option.value === "CNOT";
    });

    if (cnotOption) {
        cnotOption.disabled = numQubits < 2;
    }

    if (numQubits < 2 && gateSelect.value === "CNOT") {
        gateSelect.value = "H";
    }

    if (gateSelect.value === "CNOT") {
        controlQubitGroup.style.display = "block";
    } else {
        controlQubitGroup.style.display = "none";
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


async function runCircuit() {
    if (!pyodide) {
        statusBox.textContent = "Simulator is still loading.";
        return;
    }

    const numQubits = Number.parseInt(numQubitsSelect.value, 10);
    const shots = Number.parseInt(shotsInput.value, 10);

    if (!Number.isInteger(shots) || shots < 1) {
        statusBox.textContent = "Measurement shots must be a positive whole number.";
        return;
    }

    try {
        statusBox.textContent = "Running circuit...";
        runButton.disabled = true;

        await new Promise((resolve) => setTimeout(resolve, 0));

        pyodide.globals.set("num_qubits", numQubits);
        pyodide.globals.set("operations_json", JSON.stringify(operations));
        pyodide.globals.set("shots", shots);

        const resultJson = pyodide.runPython("run_circuit(num_qubits, operations_json, shots)");
        const result = JSON.parse(resultJson);

        displayResult(result);
        statusBox.textContent = "Circuit ran successfully.";
    } catch (error) {
        console.error(error);
        statusBox.textContent = "Error running circuit. Check the circuit settings or browser console.";
    } finally {
        runButton.disabled = false;
    }
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

function loadBellStateExample() {
    numQubitsSelect.value = "2";

    updateQubitOptions();
    updateGateControls();

    operations = [
        { gate: "H", target: 0 },
        { gate: "CNOT", control: 0, target: 1 }
    ];

    updateOperationList();

    circuitOutput.textContent = "Waiting for simulator...";
    stateOutput.textContent = "Waiting for simulator...";
    probabilityOutput.textContent = "Waiting for simulator...";
    measurementOutput.textContent = "Waiting for simulator...";

    statusBox.textContent = "Bell state example loaded. Click Run Circuit.";
}


numQubitsSelect.addEventListener("change", () => {
    operations = [];
    updateQubitOptions();
    updateGateControls();
    updateOperationList();
    statusBox.textContent = "Number of qubits changed. Circuit reset.";
});

gateSelect.addEventListener("change", updateGateControls);

addGateButton.addEventListener("click", addGate);
bellExampleButton.addEventListener("click", loadBellStateExample);
runButton.addEventListener("click", runCircuit);
resetButton.addEventListener("click", resetCircuit);

initializePyodide();