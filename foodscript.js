// ---------------------------
// Modal Elements
// ---------------------------
const loginModal = document.getElementById("loginModal");
const signupModal = document.getElementById("signupModal");
const orderModal = document.getElementById("orderModal");
const successPopup = document.getElementById("successPopup");
const reviewModal = document.getElementById("reviewModal");

// Buttons
const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");
const closeLogin = document.getElementById("closeLogin");
const closeSignup = document.getElementById("closeSignup");
const closeOrder = document.getElementById("closeOrder");
const closeSuccess = document.getElementById("closeSuccess");
const closeReview = document.getElementById("closeReview");
const addReviewBtn = document.getElementById("addReviewBtn");

// Switch forms
const toSignup = document.getElementById("toSignup");
const toLogin = document.getElementById("toLogin");

// Order fields
const orderItem = document.getElementById("orderItem");
const orderPrice = document.getElementById("orderPrice");
const quantityInput = document.getElementById("quantity");
const totalPriceInput = document.getElementById("totalPrice");

// Qty buttons
const qtyPlus = document.getElementById("qtyPlus");
const qtyMinus = document.getElementById("qtyMinus");


// ---------------------------
// Helper function – Show Modal
// ---------------------------
function showModal(modal) {
    modal.style.display = "flex";
    modal.setAttribute("aria-hidden", "false");
}

// ---------------------------
// Helper function – Hide Modal
// ---------------------------
function hideModal(modal) {
    modal.style.display = "none";
    modal.setAttribute("aria-hidden", "true");
}


// ---------------------------
// LOGIN MODAL
// ---------------------------
if (loginBtn) loginBtn.addEventListener("click", () => showModal(loginModal));
if (closeLogin) closeLogin.addEventListener("click", () => hideModal(loginModal));


// ---------------------------
// SIGNUP MODAL
// ---------------------------
if (signupBtn) signupBtn.addEventListener("click", () => showModal(signupModal));
if (closeSignup) closeSignup.addEventListener("click", () => hideModal(signupModal));


// ---------------------------
// SWITCH Login <-> Signup
// ---------------------------
if (toSignup) {
    toSignup.addEventListener("click", () => {
        hideModal(loginModal);
        showModal(signupModal);
    });
}

if (toLogin) {
    toLogin.addEventListener("click", () => {
        hideModal(signupModal);
        showModal(loginModal);
    });
}


// ---------------------------
// ORDER MODAL
// ---------------------------
document.querySelectorAll(".orderBtn").forEach(button => {
    button.addEventListener("click", () => {
        const item = button.getAttribute("data-item");
        const price = button.getAttribute("data-price");

        orderItem.value = item;
        orderPrice.value = price;

        quantityInput.value = 1;
        totalPriceInput.value = price;

        showModal(orderModal);
    });
});

if (closeOrder) closeOrder.addEventListener("click", () => hideModal(orderModal));


// ---------------------------
// QUANTITY + / - BUTTONS
// ---------------------------
if (qtyPlus) {
    qtyPlus.addEventListener("click", () => {
        let qty = parseInt(quantityInput.value) + 1;
        quantityInput.value = qty;
        updateTotal();
    });
}

if (qtyMinus) {
    qtyMinus.addEventListener("click", () => {
        let qty = parseInt(quantityInput.value);
        if (qty > 1) {
            quantityInput.value = qty - 1;
            updateTotal();
        }
    });
}


// ---------------------------
// AUTO UPDATE TOTAL
// ---------------------------
function updateTotal() {
    let price = parseInt(orderPrice.value);
    let qty = parseInt(quantityInput.value);
    totalPriceInput.value = price * qty;
}

if (quantityInput) quantityInput.addEventListener("input", updateTotal);


// ---------------------------
// ORDER SUCCESS POPUP
// ---------------------------
if (window.location.search.includes("success=1")) {
    showModal(successPopup);
}

if (closeSuccess) closeSuccess.addEventListener("click", () => hideModal(successPopup));


// ---------------------------
// REVIEW MODAL
// ---------------------------
if (addReviewBtn) {
    addReviewBtn.addEventListener("click", () => showModal(reviewModal));
}

if (closeReview) {
    closeReview.addEventListener("click", () => hideModal(reviewModal));
}


// ---------------------------
// CLOSE MODALS WHEN CLICK OUTSIDE
// ---------------------------
window.addEventListener("click", (e) => {
    if (e.target === loginModal) hideModal(loginModal);
    if (e.target === signupModal) hideModal(signupModal);
    if (e.target === orderModal) hideModal(orderModal);
    if (e.target === successPopup) hideModal(successPopup);
    if (e.target === reviewModal) hideModal(reviewModal);
});


// ---------------------------
// SEARCH FILTER
// ---------------------------
const searchInput = document.getElementById("searchInput");
const foodItems = document.querySelectorAll(".item");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {
        let value = this.value.toLowerCase();

        foodItems.forEach(item => {
            let name = item.querySelector("h4").innerText.toLowerCase();
            item.style.display = name.includes(value) ? "block" : "none";
        });
    });
}
