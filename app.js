/**
 * ROBOTICS LAB ERP & BOM ESTIMATOR — CLIENT-SIDE JAVASCRIPT CONTROLLER
 * Full OOP Polymorphic Model-View-Presenter Architecture in Vanilla JS.
 */

// Initial Seed Data (strictly matching inventory.csv from C++ core)
const INITIAL_INVENTORY = [
    { type: "Motor", name: "NEMA 17 Stepper Motor", id: "MOT-001", price: 14.50, quantity: 25, spec1: 12, spec2: 1200 },
    { type: "Motor", name: "DC Planetary Gearmotor 12V", id: "MOT-002", price: 28.75, quantity: 8, spec1: 12, spec2: 350 },
    { type: "Motor", name: "Brushless Outrunner 920KV", id: "MOT-003", price: 19.99, quantity: 14, spec1: 11, spec2: 10000 },
    { type: "Sensor", name: "RPLIDAR A1M8 360 Lidar", id: "SEN-001", price: 99.00, quantity: 5, spec1: "Optical/Laser", spec2: 12.0 },
    { type: "Sensor", name: "HC-SR04 Ultrasonic Sensor", id: "SEN-002", price: 3.25, quantity: 45, spec1: "Ultrasonic", spec2: 4.0 },
    { type: "Sensor", name: "BNO055 9-DOF IMU Sensor", id: "SEN-003", price: 34.50, quantity: 12, spec1: "Inertial", spec2: 1.5 },
    { type: "Controller", name: "STM32F407G Discovery Board", id: "CTL-001", price: 24.90, quantity: 10, spec1: "ARM Cortex-M4", spec2: 16 },
    { type: "Controller", name: "Raspberry Pi 4 Model B (4GB)", id: "CTL-002", price: 55.00, quantity: 6, spec1: "ARM Cortex-A72", spec2: 40 },
    { type: "Controller", name: "Arduino Mega 2560 Rev3", id: "CTL-003", price: 38.50, quantity: 15, spec1: "AVR RISC", spec2: 54 },
    { type: "Battery", name: "Turnigy LiPo 3S 5000mAh", id: "BAT-001", price: 42.00, quantity: 10, spec1: 5000, spec2: "LiPo" },
    { type: "Battery", name: "Panasonic 18650 Li-ion Cell", id: "BAT-002", price: 6.50, quantity: 60, spec1: 3500, spec2: "Li-Ion" },
    { type: "Battery", name: "LiFePO4 12V 10Ah Deep Cycle", id: "BAT-003", price: 89.00, quantity: 3, spec1: 10000, spec2: "LiFePO4" },
    { type: "Converter", name: "LM2596 Buck Step-Down Module", id: "CNV-001", price: 2.80, quantity: 50, spec1: 40.0, spec2: 1.25 },
    { type: "Converter", name: "XL6009 Boost Step-Up Module", id: "CNV-002", price: 3.40, quantity: 30, spec1: 32.0, spec2: 35.0 },
    { type: "Converter", name: "Pololu 5V 5A Step-Down D24V50F5", id: "CNV-003", price: 16.95, quantity: 7, spec1: 38.0, spec2: 5.0 },
    { type: "Generic", name: "M3 Standoff Hardware Kit", id: "GEN-001", price: 8.99, quantity: 18 },
    { type: "Generic", name: "Aluminum Extrusion 2020 500mm", id: "GEN-002", price: 11.20, quantity: 22 }
];

// App State
class AppState {
    constructor() {
        this.inventory = this.loadFromStorage() || JSON.parse(JSON.stringify(INITIAL_INVENTORY));
        this.bomItems = []; // { componentId, quantity }
        this.projectName = "Autonomous Mobile Robot (AMR-01)";
        this.taxRate = 0.0825;
        this.shippingCost = 15.00;
    }

    loadFromStorage() {
        try {
            const data = localStorage.getItem("oops_cbp_inventory");
            return data ? JSON.parse(data) : null;
        } catch (e) {
            return null;
        }
    }

    saveToStorage() {
        try {
            localStorage.setItem("oops_cbp_inventory", JSON.stringify(this.inventory));
        } catch (e) {}
    }

    resetData() {
        this.inventory = JSON.parse(JSON.stringify(INITIAL_INVENTORY));
        this.bomItems = [];
        this.saveToStorage();
    }

    getComponentById(id) {
        return this.inventory.find(c => c.id === id);
    }

    addComponent(comp) {
        if (this.getComponentById(comp.id)) {
            return { success: false, message: `Component ID '${comp.id}' already exists!` };
        }
        this.inventory.push(comp);
        this.saveToStorage();
        return { success: true, message: `Added ${comp.name} (${comp.id}) to catalog.` };
    }

    updateStock(id, newQty) {
        const comp = this.getComponentById(id);
        if (!comp) return false;
        comp.quantity = Math.max(0, parseInt(newQty) || 0);
        
        // Auto-bound BOM allocation if stock dropped below requirement
        const bomItem = this.bomItems.find(b => b.componentId === id);
        if (bomItem && bomItem.quantity > comp.quantity) {
            bomItem.quantity = comp.quantity;
            if (bomItem.quantity === 0) {
                this.bomItems = this.bomItems.filter(b => b.componentId !== id);
            }
        }

        this.saveToStorage();
        return true;
    }

    removeComponent(id) {
        this.inventory = this.inventory.filter(c => c.id !== id);
        this.bomItems = this.bomItems.filter(b => b.componentId !== id);
        this.saveToStorage();
        return true;
    }

    addToBOM(componentId, qty) {
        const comp = this.getComponentById(componentId);
        if (!comp) return { success: false, message: "Component not found." };

        const requestedQty = parseInt(qty) || 0;
        if (requestedQty <= 0) return { success: false, message: "Quantity must be > 0." };

        const existing = this.bomItems.find(b => b.componentId === componentId);
        const currentAlloc = existing ? existing.quantity : 0;
        const totalAlloc = currentAlloc + requestedQty;

        if (totalAlloc > comp.quantity) {
            return {
                success: false,
                message: `Insufficient stock! Requested total: ${totalAlloc}, Available in warehouse: ${comp.quantity}.`
            };
        }

        if (existing) {
            existing.quantity = totalAlloc;
        } else {
            this.bomItems.push({ componentId, quantity: requestedQty });
        }

        return { success: true, message: `Allocated ${requestedQty}x ${comp.name} to BOM.` };
    }

    removeFromBOM(componentId) {
        this.bomItems = this.bomItems.filter(b => b.componentId !== componentId);
    }

    clearBOM() {
        this.bomItems = [];
    }

    // Calculations
    getTotalValuation() {
        return this.inventory.reduce((sum, c) => sum + (c.price * c.quantity), 0);
    }

    getTotalUnits() {
        return this.inventory.reduce((sum, c) => sum + c.quantity, 0);
    }

    getLowStockItems(threshold = 10) {
        return this.inventory.filter(c => c.quantity <= threshold);
    }

    getBomSubtotal() {
        return this.bomItems.reduce((sum, b) => {
            const comp = this.getComponentById(b.componentId);
            return sum + (comp ? comp.price * b.quantity : 0);
        }, 0);
    }

    getBomTax() {
        return this.getBomSubtotal() * this.taxRate;
    }

    getBomGrandTotal() {
        const sub = this.getBomSubtotal();
        if (this.bomItems.length === 0) return 0;
        return sub + this.getBomTax() + this.shippingCost;
    }
}

// Instantiate Global State
const state = new AppState();

// ----------------------------------------------------------------------------
// VIEW HELPERS & SPECS FORMATTERS (POLYMORPHIC DISPLAY)
// ----------------------------------------------------------------------------
function formatPolymorphicSpecs(comp) {
    switch (comp.type) {
        case "Motor":
            return `<span class="specs-desc">⚡ Voltage: <strong>${comp.spec1}V</strong> | 🔄 Max: <strong>${comp.spec2} RPM</strong></span>`;
        case "Sensor":
            return `<span class="specs-desc">📡 Category: <strong>${comp.spec1}</strong> | 🎯 Range: <strong>${comp.spec2} m</strong></span>`;
        case "Controller":
            return `<span class="specs-desc">💻 Arch: <strong>${comp.spec1}</strong> | 🔌 Ports: <strong>${comp.spec2}</strong></span>`;
        case "Battery":
            return `<span class="specs-desc">🔋 Capacity: <strong>${comp.spec1} mAh</strong> | 🧪 Chem: <strong>${comp.spec2}</strong></span>`;
        case "Converter":
            return `<span class="specs-desc">⚙️ Input: <strong>${comp.spec1}V</strong> → Output: <strong>${comp.spec2}V</strong></span>`;
        default:
            return `<span class="specs-desc text-muted">Standard structural hardware</span>`;
    }
}

function getCategoryBadgeClass(type) {
    const map = {
        Motor: "badge-motor",
        Sensor: "badge-sensor",
        Controller: "badge-controller",
        Battery: "badge-battery",
        Converter: "badge-converter",
        Generic: "badge-generic"
    };
    return map[type] || "badge-generic";
}

function showToast(message, isError = false) {
    const container = document.getElementById("toastContainer");
    const toast = document.createElement("div");
    toast.className = `toast ${isError ? 'error' : 'success'}`;
    toast.innerHTML = `<span>${isError ? '⚠️' : '✓'}</span> <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 250);
    }, 3500);
}

// ----------------------------------------------------------------------------
// UI RENDERERS
// ----------------------------------------------------------------------------

// 1. Dashboard Tab
function renderDashboard() {
    // KPI Cards
    const totalVal = state.getTotalValuation();
    document.getElementById("kpiTotalValuation").textContent = `$${totalVal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    document.getElementById("kpiUniqueSkus").textContent = state.inventory.length;
    document.getElementById("kpiTotalUnits").textContent = state.getTotalUnits().toLocaleString();

    const lowStock = state.getLowStockItems(10);
    document.getElementById("kpiLowStockCount").textContent = lowStock.length;

    // Badges in Nav
    document.getElementById("badgeCatalogCount").textContent = state.inventory.length;
    document.getElementById("badgeBomCount").textContent = state.bomItems.length;

    // Category Distribution Bars
    const catCounts = {};
    const catColors = {
        Motor: "#38bdf8",
        Sensor: "#34d399",
        Controller: "#818cf8",
        Battery: "#fbbf24",
        Converter: "#c084fc",
        Generic: "#94a3b8"
    };

    state.inventory.forEach(c => {
        catCounts[c.type] = (catCounts[c.type] || 0) + c.quantity;
    });

    const totalUnits = state.getTotalUnits() || 1;
    const catListEl = document.getElementById("categoryBreakdownList");
    catListEl.innerHTML = "";

    const categories = ["Motor", "Sensor", "Controller", "Battery", "Converter", "Generic"];
    categories.forEach(cat => {
        const units = catCounts[cat] || 0;
        const percent = Math.round((units / totalUnits) * 100);
        const color = catColors[cat] || "#38bdf8";

        const item = document.createElement("div");
        item.className = "cat-item";
        item.innerHTML = `
            <div class="cat-info">
                <span><strong>${cat}</strong> (${units} units)</span>
                <span style="color: ${color}; font-weight: 700;">${percent}%</span>
            </div>
            <div class="cat-bar-bg">
                <div class="cat-bar-fill" style="width: ${percent}%; background-color: ${color};"></div>
            </div>
        `;
        catListEl.appendChild(item);
    });

    // Low Stock Radar Table
    const lowStockTbody = document.getElementById("lowStockTableBody");
    lowStockTbody.innerHTML = "";

    if (lowStock.length === 0) {
        lowStockTbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted" style="padding: 24px;">All components have sufficient stock levels (> 10 units).</td></tr>`;
    } else {
        lowStock.forEach(c => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>
                    <div class="component-name-cell">${c.name}</div>
                    <code class="code-id">${c.id}</code>
                </td>
                <td><span class="badge ${getCategoryBadgeClass(c.type)}">${c.type}</span></td>
                <td><span class="stock-num low">${c.quantity}</span></td>
                <td><span class="badge badge-warning">Shortage</span></td>
                <td>
                    <button class="btn btn-secondary-sm" onclick="quickRestock('${c.id}', 10)">
                        +10 Restock
                    </button>
                </td>
            `;
            lowStockTbody.appendChild(tr);
        });
    }
}

// 2. Hardware Catalog Tab
function renderCatalog() {
    const tbody = document.getElementById("catalogTableBody");
    const searchQuery = (document.getElementById("catalogSearchInput").value || "").toLowerCase().trim();
    const filterCat = document.getElementById("filterCategorySelect").value;

    const filtered = state.inventory.filter(c => {
        const matchesCat = filterCat === "All" || c.type === filterCat;
        const matchesSearch = !searchQuery || 
            c.name.toLowerCase().includes(searchQuery) ||
            c.id.toLowerCase().includes(searchQuery) ||
            c.type.toLowerCase().includes(searchQuery) ||
            (c.spec1 && String(c.spec1).toLowerCase().includes(searchQuery)) ||
            (c.spec2 && String(c.spec2).toLowerCase().includes(searchQuery));
        return matchesCat && matchesSearch;
    });

    tbody.innerHTML = "";

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted" style="padding: 30px;">No components match your search filter criteria.</td></tr>`;
        return;
    }

    filtered.forEach(c => {
        const totalItemVal = (c.price * c.quantity).toFixed(2);
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><span class="badge ${getCategoryBadgeClass(c.type)}">${c.type}</span></td>
            <td><span class="component-name-cell">${c.name}</span></td>
            <td><code class="code-id">${c.id}</code></td>
            <td>${formatPolymorphicSpecs(c)}</td>
            <td class="numeric-cell">$${c.price.toFixed(2)}</td>
            <td>
                <div class="stock-stepper-cell">
                    <button class="btn-action-icon" onclick="adjustStock('${c.id}', -1)" title="Decrease stock">-</button>
                    <span class="stock-num ${c.quantity <= 10 ? 'low' : ''}">${c.quantity}</span>
                    <button class="btn-action-icon" onclick="adjustStock('${c.id}', 1)" title="Increase stock">+</button>
                </div>
            </td>
            <td class="numeric-cell" style="font-weight: 700; color: #38bdf8;">$${totalItemVal}</td>
            <td>
                <div style="display: flex; gap: 6px;">
                    <button class="btn-action-icon" onclick="openAddToBomDirect('${c.id}')" title="Allocate to Project BOM">🤖</button>
                    <button class="btn-action-icon danger" onclick="deleteComponent('${c.id}')" title="Delete Component">🗑️</button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// 3. Project BOM Tab
function renderBOM() {
    // Project Config Fields
    document.getElementById("inputProjectName").value = state.projectName;
    document.getElementById("inputTaxRate").value = (state.taxRate * 100).toFixed(2);
    document.getElementById("inputShippingCost").value = state.shippingCost.toFixed(2);

    // Component Dropdown in BOM Form
    const selectEl = document.getElementById("selectBomComponent");
    const currentVal = selectEl.value;
    selectEl.innerHTML = "";

    state.inventory.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c.id;
        opt.textContent = `[${c.type}] ${c.name} (${c.id}) — In Stock: ${c.quantity}`;
        selectEl.appendChild(opt);
    });

    if (currentVal && state.getComponentById(currentVal)) {
        selectEl.value = currentVal;
    }

    updateBomSelectedComponentInfo();

    // BOM Table
    const tbody = document.getElementById("bomTableBody");
    tbody.innerHTML = "";

    if (state.bomItems.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted" style="padding: 30px;">No components added to this robotics build yet. Select a hardware item on the left to allocate.</td></tr>`;
    } else {
        state.bomItems.forEach(item => {
            const comp = state.getComponentById(item.componentId);
            if (!comp) return;

            const lineTotal = (comp.price * item.quantity).toFixed(2);
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>
                    <div class="component-name-cell">${comp.name}</div>
                    <code class="code-id">${comp.id}</code>
                </td>
                <td><span class="badge ${getCategoryBadgeClass(comp.type)}">${comp.type}</span></td>
                <td class="numeric-cell">$${comp.price.toFixed(2)}</td>
                <td>
                    <div class="stock-stepper-cell">
                        <button class="btn-action-icon" onclick="adjustBomQty('${comp.id}', -1)">-</button>
                        <span class="stock-num">${item.quantity}</span>
                        <button class="btn-action-icon" onclick="adjustBomQty('${comp.id}', 1)">+</button>
                    </div>
                </td>
                <td class="numeric-cell" style="font-weight: 700; color: #34d399;">$${lineTotal}</td>
                <td>
                    <button class="btn-action-icon danger" onclick="removeBomItem('${comp.id}')" title="Remove from BOM">🗑️</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Financial Breakdown
    const subtotal = state.getBomSubtotal();
    const tax = state.getBomTax();
    const grand = state.getBomGrandTotal();

    document.getElementById("bomSubtotal").textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById("bomTaxLabel").textContent = `Estimated Sales Tax (${(state.taxRate * 100).toFixed(2)}%):`;
    document.getElementById("bomTax").textContent = `$${tax.toFixed(2)}`;
    document.getElementById("bomShipping").textContent = `$${state.shippingCost.toFixed(2)}`;
    document.getElementById("bomGrandTotal").textContent = `$${grand.toFixed(2)}`;
}

function updateBomSelectedComponentInfo() {
    const selId = document.getElementById("selectBomComponent").value;
    const comp = state.getComponentById(selId);
    if (comp) {
        const existing = state.bomItems.find(b => b.componentId === selId);
        const allocated = existing ? existing.quantity : 0;
        const availableRem = Math.max(0, comp.quantity - allocated);

        document.getElementById("bomSelectedStock").textContent = `${comp.quantity} units (Available: ${availableRem})`;
        document.getElementById("bomSelectedPrice").textContent = `$${comp.price.toFixed(2)}`;
    }
}

// 4. Persistence Tab
function renderPersistence() {
    const csvContent = generateCSVString();
    document.getElementById("csvStreamViewer").textContent = csvContent;

    const invoiceContent = generateInvoiceReceiptString();
    document.getElementById("invoiceStreamViewer").textContent = invoiceContent;
}

function generateCSVString() {
    return state.inventory.map(c => {
        let line = `${c.type},${c.name},${c.id},${c.price.toFixed(6)},${c.quantity}`;
        if (c.type === "Motor") line += `,${c.spec1},${c.spec2}`;
        else if (c.type === "Sensor") line += `,${c.spec1},${Number(c.spec2).toFixed(6)}`;
        else if (c.type === "Controller") line += `,${c.spec1},${c.spec2}`;
        else if (c.type === "Battery") line += `,${c.spec1},${c.spec2}`;
        else if (c.type === "Converter") line += `,${Number(c.spec1).toFixed(6)},${Number(c.spec2).toFixed(6)}`;
        return line;
    }).join("\n");
}

function generateInvoiceReceiptString() {
    const now = new Date().toISOString().split("T")[0];
    let txt = `==========================================================================\n`;
    txt += `             OFFICIAL ROBOTICS HARDWARE QUOTE & RECEIPT                  \n`;
    txt += `==========================================================================\n`;
    txt += `Project Name      : ${state.projectName}\n`;
    txt += `Generated Date    : ${now}\n`;
    txt += `Inventory System  : Robotics Laboratory ERP [Phase 4 / OOPS CBP]\n`;
    txt += `--------------------------------------------------------------------------\n`;
    txt += `Hardware Component                 | ID       | Unit Price | Qty   | Line Total \n`;
    txt += `--------------------------------------------------------------------------\n`;

    if (state.bomItems.length === 0) {
        txt += `(No components allocated to this project build yet)\n`;
    } else {
        state.bomItems.forEach(b => {
            const comp = state.getComponentById(b.componentId);
            if (!comp) return;
            const lineTotal = (comp.price * b.quantity).toFixed(2);
            const namePad = comp.name.padEnd(34, " ").substring(0, 34);
            const idPad = comp.id.padEnd(8, " ");
            const pricePad = `$${comp.price.toFixed(2)}`.padStart(10, " ");
            const qtyPad = `${b.quantity}`.padStart(5, " ");
            const totPad = `$${lineTotal}`.padStart(10, " ");
            txt += `${namePad} | ${idPad} | ${pricePad} | ${qtyPad} | ${totPad}\n`;
        });
    }

    txt += `==========================================================================\n`;
    txt += `  Subtotal                  : $${state.getBomSubtotal().toFixed(2)}\n`;
    txt += `  Estimated Tax (${(state.taxRate * 100).toFixed(2)}%)      : $${state.getBomTax().toFixed(2)}\n`;
    txt += `  Shipping & Logistics      : $${state.shippingCost.toFixed(2)}\n`;
    txt += `  ----------------------------------------------------------------------\n`;
    txt += `  FINAL TOTAL ESTIMATED COST: $${state.getBomGrandTotal().toFixed(2)}\n`;
    txt += `==========================================================================\n`;
    txt += `Authorized Signature: __________________________   Date: _________________\n`;
    return txt;
}

// Master Refresh
function refreshAll() {
    renderDashboard();
    renderCatalog();
    renderBOM();
    renderPersistence();
    updateFooterMessage();
}

function updateFooterMessage(msg = null) {
    const el = document.getElementById("footerStatusMsg");
    if (msg) {
        el.textContent = msg;
    } else {
        el.textContent = `System synchronized. ${state.inventory.length} polymorphic hardware SKUs loaded.`;
    }
}

// ----------------------------------------------------------------------------
// INTERACTIVE ACTIONS & HANDLERS
// ----------------------------------------------------------------------------
function adjustStock(id, delta) {
    const comp = state.getComponentById(id);
    if (!comp) return;
    const newQty = Math.max(0, comp.quantity + delta);
    state.updateStock(id, newQty);
    refreshAll();
    showToast(`Updated ${comp.id} stock to ${newQty} units.`);
}

function quickRestock(id, amount) {
    adjustStock(id, amount);
}

function deleteComponent(id) {
    const comp = state.getComponentById(id);
    if (!comp) return;
    if (confirm(`Are you sure you want to delete '${comp.name}' (${comp.id})?`)) {
        state.removeComponent(id);
        refreshAll();
        showToast(`Removed component ${id} from catalog.`, true);
    }
}

function openAddToBomDirect(id) {
    switchTab("tabBOM");
    document.getElementById("selectBomComponent").value = id;
    updateBomSelectedComponentInfo();
}

function adjustBomQty(id, delta) {
    const comp = state.getComponentById(id);
    const item = state.bomItems.find(b => b.componentId === id);
    if (!comp || !item) return;

    const newQty = item.quantity + delta;
    if (newQty <= 0) {
        state.removeFromBOM(id);
        showToast(`Removed ${comp.name} from project build.`);
    } else if (newQty > comp.quantity) {
        showToast(`Cannot exceed in-stock quantity (${comp.quantity} available).`, true);
        return;
    } else {
        item.quantity = newQty;
    }
    refreshAll();
}

function removeBomItem(id) {
    state.removeFromBOM(id);
    refreshAll();
    showToast(`Removed item from BOM.`);
}

// Navigation Tabs
function switchTab(targetId) {
    document.querySelectorAll(".nav-tab").forEach(tab => {
        tab.classList.toggle("active", tab.dataset.tab === targetId);
    });
    document.querySelectorAll(".tab-content").forEach(content => {
        content.classList.toggle("active", content.id === targetId);
    });
}

// ----------------------------------------------------------------------------
// INITIALIZATION & EVENT LISTENERS
// ----------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    // Tab Clicks
    document.querySelectorAll(".nav-tab").forEach(tab => {
        tab.addEventListener("click", () => switchTab(tab.dataset.tab));
    });

    // Catalog Search & Filter
    document.getElementById("catalogSearchInput").addEventListener("input", renderCatalog);
    document.getElementById("filterCategorySelect").addEventListener("change", renderCatalog);

    // BOM Component Dropdown Change
    document.getElementById("selectBomComponent").addEventListener("change", updateBomSelectedComponentInfo);

    // BOM Stepper
    document.getElementById("btnBomQtyInc").addEventListener("click", () => {
        const inp = document.getElementById("inputBomQuantity");
        inp.value = (parseInt(inp.value) || 0) + 1;
    });
    document.getElementById("btnBomQtyDec").addEventListener("click", () => {
        const inp = document.getElementById("inputBomQuantity");
        inp.value = Math.max(1, (parseInt(inp.value) || 1) - 1);
    });

    // Add to BOM Button
    document.getElementById("btnAddToBom").addEventListener("click", () => {
        const selId = document.getElementById("selectBomComponent").value;
        const qty = parseInt(document.getElementById("inputBomQuantity").value) || 1;
        const res = state.addToBOM(selId, qty);
        showToast(res.message, !res.success);
        if (res.success) {
            refreshAll();
        }
    });

    // Clear BOM
    document.getElementById("btnClearBom").addEventListener("click", () => {
        if (confirm("Clear all hardware allocations from this robotics project?")) {
            state.clearBOM();
            refreshAll();
            showToast("BOM cleared.");
        }
    });

    // Project Name & Margins Config Change
    document.getElementById("inputProjectName").addEventListener("input", (e) => {
        state.projectName = e.target.value.trim() || "Robotics Build";
        renderPersistence();
    });
    document.getElementById("inputTaxRate").addEventListener("input", (e) => {
        state.taxRate = (parseFloat(e.target.value) || 0) / 100.0;
        renderBOM();
        renderPersistence();
    });
    document.getElementById("inputShippingCost").addEventListener("input", (e) => {
        state.shippingCost = parseFloat(e.target.value) || 0;
        renderBOM();
        renderPersistence();
    });

    // Add Component Modal
    const modal = document.getElementById("modalAddComponent");
    const openModalBtn = document.getElementById("btnOpenAddModal");
    const closeModalBtn = document.getElementById("btnCloseModal");
    const cancelModalBtn = document.getElementById("btnCancelModal");

    openModalBtn.addEventListener("click", () => {
        modal.classList.add("active");
    });

    const closeModal = () => modal.classList.remove("active");
    closeModalBtn.addEventListener("click", closeModal);
    cancelModalBtn.addEventListener("click", closeModal);

    // Dynamic category selector in modal
    const catSelect = document.getElementById("modalSelectCategory");
    catSelect.addEventListener("change", (e) => {
        const val = e.target.value;
        document.querySelectorAll(".subclass-fields").forEach(el => el.classList.remove("active"));
        const targetSection = document.getElementById(`subclass${val}`);
        if (targetSection) targetSection.classList.add("active");
    });

    // Submit Add Component Form
    document.getElementById("formAddComponent").addEventListener("submit", (e) => {
        e.preventDefault();
        const type = catSelect.value;
        const name = document.getElementById("modalInputName").value.trim();
        const id = document.getElementById("modalInputId").value.trim().toUpperCase();
        const price = parseFloat(document.getElementById("modalInputPrice").value) || 0;
        const quantity = parseInt(document.getElementById("modalInputQuantity").value) || 0;

        let spec1 = null, spec2 = null;
        if (type === "Motor") {
            spec1 = parseInt(document.getElementById("motorVoltage").value) || 12;
            spec2 = parseInt(document.getElementById("motorRpm").value) || 1000;
        } else if (type === "Sensor") {
            spec1 = document.getElementById("sensorType").value.trim() || "Optical";
            spec2 = parseFloat(document.getElementById("sensorRange").value) || 1.0;
        } else if (type === "Controller") {
            spec1 = document.getElementById("ctlArch").value.trim() || "ARM Cortex-M4";
            spec2 = parseInt(document.getElementById("ctlPorts").value) || 16;
        } else if (type === "Battery") {
            spec1 = parseInt(document.getElementById("batCapacity").value) || 5000;
            spec2 = document.getElementById("batChem").value.trim() || "LiPo";
        } else if (type === "Converter") {
            spec1 = parseFloat(document.getElementById("cnvInputV").value) || 36.0;
            spec2 = parseFloat(document.getElementById("cnvOutputV").value) || 5.0;
        }

        const comp = { type, name, id, price, quantity, spec1, spec2 };
        const res = state.addComponent(comp);

        showToast(res.message, !res.success);
        if (res.success) {
            closeModal();
            document.getElementById("formAddComponent").reset();
            refreshAll();
        }
    });

    // OOP Guide Modal
    const oopModal = document.getElementById("modalOopGuide");
    document.getElementById("btnOopGuide").addEventListener("click", () => oopModal.classList.add("active"));
    document.getElementById("btnCloseOopGuide").addEventListener("click", () => oopModal.classList.remove("active"));

    // Reset Data
    document.getElementById("btnResetData").addEventListener("click", () => {
        if (confirm("Reset hardware catalog to initial sample data from inventory.csv?")) {
            state.resetData();
            refreshAll();
            showToast("Hardware catalog reset to default sample records.");
        }
    });

    // Download Updated CSV
    document.getElementById("btnDownloadCsv").addEventListener("click", () => {
        const csvStr = generateCSVString();
        const blob = new Blob([csvStr], { type: "text/csv;charset=utf-8;" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "inventory.csv";
        link.click();
        showToast("Downloaded updated inventory.csv");
    });

    // Export TXT Invoice
    document.getElementById("btnExportInvoiceTxt").addEventListener("click", () => {
        const txt = generateInvoiceReceiptString();
        const blob = new Blob([txt], { type: "text/plain;charset=utf-8;" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "project_receipt.txt";
        link.click();
        showToast("Exported project invoice receipt.");
    });

    // Copy CSV to Clipboard
    document.getElementById("btnCopyCsv").addEventListener("click", () => {
        const csvStr = generateCSVString();
        navigator.clipboard.writeText(csvStr).then(() => {
            showToast("CSV data copied to clipboard!");
        });
    });

    // Custom CSV Upload
    document.getElementById("csvFileInput").addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            const lines = event.target.result.split(/\r?\n/);
            const imported = [];
            lines.forEach(line => {
                if (!line.trim()) return;
                const tokens = line.split(",");
                if (tokens.length < 5) return;
                const type = tokens[0].trim();
                const name = tokens[1].trim();
                const id = tokens[2].trim();
                const price = parseFloat(tokens[3]) || 0;
                const quantity = parseInt(tokens[4]) || 0;
                const spec1 = tokens[5] ? tokens[5].trim() : null;
                const spec2 = tokens[6] ? tokens[6].trim() : null;
                imported.push({ type, name, id, price, quantity, spec1, spec2 });
            });

            if (imported.length > 0) {
                state.inventory = imported;
                state.saveToStorage();
                refreshAll();
                showToast(`Successfully imported ${imported.length} components from CSV!`);
            } else {
                showToast("Could not parse components from uploaded file.", true);
            }
        };
        reader.readAsText(file);
    });

    // Clock in footer
    setInterval(() => {
        const d = new Date();
        const dateStr = d.toISOString().split("T")[0];
        const timeStr = d.toTimeString().split(" ")[0];
        document.getElementById("footerClock").textContent = `🕒 ${dateStr} ${timeStr}`;
    }, 1000);

    // Initial render
    refreshAll();
});
