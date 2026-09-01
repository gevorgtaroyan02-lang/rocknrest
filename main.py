import http.server
import socketserver
import webbrowser

PORT = 8000

html_content = """
<!DOCTYPE html>
<html lang="hy">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rock N Rest - App & Admin</title>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; }
        body { background-color: #f6f6f9; padding-bottom: 70px; color: #2c2c2c; }

        .header { background: #4a3525; padding: 12px 16px 16px 16px; color: white; position: sticky; top: 0; z-index: 100; }
        .location { font-size: 13px; opacity: 0.9; display: flex; align-items: center; gap: 4px; margin-bottom: 10px; }
        .search-box { background: white; border-radius: 25px; padding: 8px 16px; display: flex; align-items: center; gap: 10px; }
        .search-box input { border: none; outline: none; width: 100%; font-size: 14px; }

        .page { display: none; padding: 16px; }
        .page.active { display: block; }

        .banner { background: linear-gradient(135deg, #6b4c35, #312115); border-radius: 16px; padding: 20px; color: white; display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
        .section-title { font-size: 18px; font-weight: bold; margin-bottom: 12px; }
        .products-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .product-card { background: white; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
        .img-container { width: 100%; height: 140px; background: #eef0f2; position: relative; }
        .img-container img { width: 100%; height: 100%; object-fit: cover; }
        .product-info { padding: 10px; }
        .product-title { font-size: 13px; font-weight: 500; margin-bottom: 6px; }
        .card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 4px; }
        
        .add-cart-btn { background: #4a3525; color: white; border: none; border-radius: 8px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer; }

        .admin-badge { background: #d32f2f; color: white; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-left: 8px; }
        .admin-item-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; }
        .user-card-item { background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 10px; padding: 12px; margin-bottom: 10px; font-size: 13px; }
        .btn-danger { background: #d32f2f; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; }

        .auth-card, .cart-card { background: white; border-radius: 16px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 16px; }
        .input-group { margin-bottom: 14px; }
        .input-group label { display: block; font-size: 12px; color: #666; margin-bottom: 6px; }
        .input-group input, .input-group select, .input-group textarea { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; outline: none; background: white; }
        
        .password-container { position: relative; width: 100%; }
        .password-container input { width: 100%; padding-right: 40px; }
        .eye-btn { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); cursor: pointer; color: #666; display: flex; align-items: center; justify-content: center; }

        .btn-primary { width: 100%; background: #4a3525; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 14px; cursor: pointer; }

        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; background: white; border-top: 1px solid #eee; display: flex; justify-content: space-around; padding: 8px 0; z-index: 1000; }
        .nav-item { display: flex; flex-direction: column; align-items: center; color: #8e8e93; font-size: 11px; text-decoration: none; cursor: pointer; position: relative; flex: 1; }
        .nav-item.active { color: #4a3525; font-weight: bold; }
        .badge-count { position: absolute; top: -4px; right: 18px; background: #e63946; color: white; font-size: 10px; padding: 1px 5px; border-radius: 10px; font-weight: bold; }

        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 2000; justify-content: center; align-items: center; }
        .modal-content { background: white; padding: 20px; border-radius: 16px; width: 90%; max-width: 420px; max-height: 90vh; overflow-y: auto; }
    </style>
</head>
<body>

    <div class="header">
        <div class="location">
            <i data-lucide="map-pin" size="14"></i>
            <span id="header-address-text">Ընտրեք հասցեն (Պրոֆիլից)</span>
        </div>
        <div class="search-box">
            <i data-lucide="search" size="18" color="#8e8e93"></i>
            <input type="text" placeholder="Փնտրել Rock N Rest-ում">
        </div>
    </div>

    <!-- PAGE 1: HOME -->
    <div id="page-home" class="page active">
        <div class="banner">
            <div>
                <h2 id="banner-title-text">Առաքում 1 օրում</h2>
                <p id="banner-subtitle-text" style="font-size: 12px; opacity: 0.8;">Երաշխավորված որակ</p>
            </div>
            <i data-lucide="armchair" size="40" color="#d4a373"></i>
        </div>

        <div class="section-title">Ապրանքներ</div>
        <div class="products-grid" id="products-grid-container"></div>
    </div>

    <!-- PAGE 2: CATALOG -->
    <div id="page-catalog" class="page">
        <div class="section-title">Կատեգորիաներ</div>
        <div class="auth-card" style="display: flex; gap: 12px; align-items: center;">
            <i data-lucide="armchair" size="24" color="#4a3525"></i>
            <div><strong>Ճոճաթոռներ</strong></div>
        </div>
    </div>

    <!-- PAGE 3: CART -->
    <div id="page-cart" class="page">
        <div class="section-title">Զամբյուղ</div>
        <div id="cart-items" class="cart-card">
            <p style="color: #666; font-size: 14px;">Զամբյուղը դատարկ է</p>
        </div>
        <div id="cart-summary" class="auth-card" style="display: none;">
            <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 12px;">
                <span>Ընդհանուր՝</span>
                <span id="total-price">0 ֏</span>
            </div>
            <button class="btn-primary" onclick="openPaymentModal()">Անցնել Վճարման</button>
        </div>
    </div>

    <!-- PAGE 4: PROFILE -->
    <div id="page-profile" class="page">
        <div class="section-title">Անձնական Էջ</div>
        
        <div id="user-profile-view" style="display: none;">
            <div class="auth-card">
                <div style="text-align: center; margin-bottom: 16px;">
                    <i data-lucide="user-check" size="48" color="#2e7d32"></i>
                    <h3 id="logged-email">user@mail.com</h3>
                </div>
                <div style="border-top: 1px solid #eee; padding-top: 12px; font-size: 13px; color: #444;">
                    <p style="margin-bottom: 6px;"><strong>📱 Հեռախոս՝</strong> <span id="profile-phone-text">-</span></p>
                    <p><strong>📍 Առաքման հասցե՝</strong> <span id="profile-address-text">-</span></p>
                </div>
                <button class="btn-primary" style="background: #c62828; margin-top: 20px;" onclick="logout()">Դուրս գալ</button>
            </div>
        </div>

        <div id="auth-form-view" class="auth-card">
            <h3 style="margin-bottom: 12px;">Գրանցում / Մուտք</h3>
            <div class="input-group">
                <label>Էլ․ հասցե (Email) *</label>
                <input type="email" id="email-input" placeholder="example@mail.com">
            </div>
            <div class="input-group">
                <label>Հեռախոսահամար *</label>
                <input type="tel" id="phone-input" placeholder="+374 99 123456">
            </div>
            <div class="input-group">
                <label>Ընտրեք Մարզը *</label>
                <select id="region-select" onchange="onRegionChange()">
                    <option value="">-- Ընտրել Մարզը --</option>
                </select>
            </div>
            <div class="input-group">
                <label>Ընտրեք Քաղաքը / Գյուղը *</label>
                <select id="city-select" disabled>
                    <option value="">-- Սկզբում ընտրեք մարզը --</option>
                </select>
            </div>
            <div class="input-group">
                <label>Փողոց, Շենք, Բնակարան *</label>
                <input type="text" id="street-input" placeholder="օրինակ՝ Աբովյան փ․, շենք 12, բն․ 4">
            </div>
            <button class="btn-primary" onclick="login()">Գրանցվել / Մուտք</button>
        </div>
    </div>

    <!-- PAGE 5: ADMIN PANEL -->
    <div id="page-admin" class="page">
        <div id="admin-auth-view" class="auth-card">
            <h3 style="margin-bottom: 12px; color: #d32f2f; display:flex; align-items:center; gap:6px;">
                <i data-lucide="lock" size="20"></i> Ադմինի Մուտք
            </h3>
            <p style="font-size: 12px; color: #666; margin-bottom: 14px;">Մուտքագրեք ադմինիստրատորի գաղտնաբառը</p>
            
            <div class="input-group">
                <label>Գաղտնաբառ</label>
                <div class="password-container">
                    <input type="password" id="admin-pass-input" placeholder="••••••••">
                    <span class="eye-btn" onclick="togglePasswordVisibility()">
                        <i id="eye-icon" data-lucide="eye" size="20"></i>
                    </span>
                </div>
            </div>
            
            <button class="btn-primary" style="background: #d32f2f;" onclick="checkAdminPassword()">Մուտք Գործել</button>
        </div>

        <div id="admin-dashboard-view" style="display: none;">
            <div class="section-title">Ադմինի Վահանակ <span class="admin-badge">ADMIN</span></div>

            <div class="auth-card">
                <h4 style="margin-bottom: 12px; color: #4a3525;">👤 Գրանցված Օգտատերեր (<span id="users-count">0</span>)</h4>
                <div id="admin-users-list"></div>
            </div>

            <div class="auth-card">
                <h4 style="margin-bottom: 12px; color: #4a3525;">✏️ Խմբագրել Գլխավոր Banner-ը</h4>
                <div class="input-group">
                    <label>Գլխավոր Վերնագիր</label>
                    <input type="text" id="admin-b-title" value="Առաքում 1 օրում">
                </div>
                <div class="input-group">
                    <label>Ենթավերնագիր</label>
                    <input type="text" id="admin-b-subtitle" value="Երաշխավորված որակ">
                </div>
                <button class="btn-primary" onclick="adminUpdateBanner()">Թարմացնել Banner-ը</button>
            </div>

            <div class="auth-card">
                <h4 style="margin-bottom: 12px; color: #4a3525;">➕ Ավելացնել Նոր Ապրանք</h4>
                <div class="input-group">
                    <label>Ապրանքի Անվանում</label>
                    <input type="text" id="admin-p-title" placeholder="օրինակ՝ Փայտե Ճոճաթոռ">
                </div>
                <div class="input-group">
                    <label>Գին (֏)</label>
                    <input type="number" id="admin-p-price" placeholder="55000">
                </div>
                <div class="input-group">
                    <label>Նկարի URL (Link)</label>
                    <input type="text" id="admin-p-img" placeholder="https://picsum.photos/400/300">
                </div>
                <button class="btn-primary" style="background: #2e7d32;" onclick="adminAddProduct()">Ավելացնել Ապրանքը</button>
            </div>

            <div class="auth-card">
                <h4 style="margin-bottom: 12px; color: #4a3525;">🗑️ Կառավարել Ապրանքները</h4>
                <div id="admin-product-list"></div>
            </div>

            <button class="btn-primary" style="background: #555; margin-top: 10px;" onclick="adminLogout()">Դուրս գալ Ադմինից</button>
        </div>
    </div>

    <!-- PAYMENT MODAL -->
    <div id="payment-modal" class="modal">
        <div class="modal-content">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h3>💳 Վճարում Բանկային Քարտով</h3>
                <i data-lucide="x" size="20" style="cursor: pointer;" onclick="closePaymentModal()"></i>
            </div>
            
            <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 14px; font-size: 12px; color: #555;">
                <strong>📍 Առաքման հասցե՝</strong> <span id="pay-modal-address">Լրացված չէ</span><br>
                <strong>📱 Հեռախոս՝</strong> <span id="pay-modal-phone">Լրացված չէ</span>
            </div>

            <div class="input-group">
                <label>Քարտի Համար</label>
                <input type="text" id="card-number" placeholder="4571 •••• •••• ••••" maxlength="19">
            </div>
            
            <div style="display: flex; gap: 10px;">
                <div class="input-group" style="flex: 1;">
                    <label>Ժամկետ (MM/YY)</label>
                    <input type="text" id="card-expiry" placeholder="12/28" maxlength="5">
                </div>
                <div class="input-group" style="flex: 1;">
                    <label>CVC / CVV</label>
                    <input type="password" id="card-cvc" placeholder="•••" maxlength="3">
                </div>
            </div>

            <button class="btn-primary" style="background: #2e7d32;" onclick="processPayment()">Վճարել Անվտանգ</button>
        </div>
    </div>

    <!-- BOTTOM NAVIGATION -->
    <div class="bottom-nav">
        <div class="nav-item active" onclick="switchPage('home', this)">
            <i data-lucide="home" size="20"></i>
            <span>Գլխավոր</span>
        </div>
        <div class="nav-item" onclick="switchPage('catalog', this)">
            <i data-lucide="layout-grid" size="20"></i>
            <span>Կատալոգ</span>
        </div>
        <div class="nav-item" onclick="switchPage('cart', this)">
            <i data-lucide="shopping-cart" size="20"></i>
            <span id="cart-badge" class="badge-count" style="display:none;">0</span>
            <span>Զամբյուղ</span>
        </div>
        <div class="nav-item" onclick="switchPage('profile', this)">
            <i data-lucide="user" size="20"></i>
            <span>Պրոֆիլ</span>
        </div>
        <div class="nav-item" onclick="switchPage('admin', this)">
            <i data-lucide="settings" size="20" color="#d32f2f"></i>
            <span style="color: #d32f2f; font-weight: bold;">Ադմին</span>
        </div>
    </div>

    <script>
        lucide.createIcons();

        const ADMIN_SECRET_PASS = "Ti7@gran";
        const FALLBACK_IMG = "https://picsum.photos/400/300";

        let products = [
            { id: 1, title: 'Վինտաժային Ճոճաթոռ', price: 45000, img: 'https://picsum.photos/id/1069/400/300' },
            { id: 2, title: 'Փափուկ Բազկաթոռ', price: 68000, img: 'https://picsum.photos/id/1070/400/300' }
        ];

        let registeredUsersList = [];
        let cart = [];
        let userData = { email: '', phone: '', address: '' };

        const locationsData = {
            "Երևան": ["Կենտրոն", "Արաբկիր", "Աջափնյակ", "Ավան", "Դավթաշեն", "Էրեբունի", "Մալաթիա-Սեբաստիա", "Նոր Նորք", "Նորք-Մարաշ", "Նուբարաշեն", "Շենգավիթ", "Քանաքեռ-Զեյթուն"],
            "Շիրակ": ["Գյումրի", "Արթիկ", "Մարալիկ"],
            "Լոռի": ["Վանաձոր", "Ստեփանավան"],
            "Կոտայք": ["Աբովյան", "Հրազդան", "Ծաղկաձոր"]
        };

        const regionSelect = document.getElementById('region-select');
        for (let region in locationsData) {
            let option = document.createElement('option');
            option.value = region;
            option.textContent = region;
            regionSelect.appendChild(option);
        }

        function onRegionChange() {
            const selectedRegion = regionSelect.value;
            const citySelect = document.getElementById('city-select');
            citySelect.innerHTML = '<option value="">-- Ընտրել Քաղաքը / Գյուղը --</option>';

            if (selectedRegion && locationsData[selectedRegion]) {
                citySelect.disabled = false;
                locationsData[selectedRegion].forEach(city => {
                    let option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            } else {
                citySelect.disabled = true;
            }
        }

        function togglePasswordVisibility() {
            const passInput = document.getElementById('admin-pass-input');
            const eyeIcon = document.getElementById('eye-icon');
            
            if (passInput.type === "password") {
                passInput.type = "text";
                eyeIcon.setAttribute('data-lucide', 'eye-off');
            } else {
                passInput.type = "password";
                eyeIcon.setAttribute('data-lucide', 'eye');
            }
            lucide.createIcons();
        }

        function checkAdminPassword() {
            const pass = document.getElementById('admin-pass-input').value;
            if (pass === ADMIN_SECRET_PASS) {
                document.getElementById('admin-auth-view').style.display = 'none';
                document.getElementById('admin-dashboard-view').style.display = 'block';
                document.getElementById('admin-pass-input').value = '';
            } else {
                alert('❌ Սխալ գաղտնաբառ');
            }
        }

        function adminLogout() {
            document.getElementById('admin-auth-view').style.display = 'block';
            document.getElementById('admin-dashboard-view').style.display = 'none';
        }

        function adminUpdateBanner() {
            const title = document.getElementById('admin-b-title').value;
            const subtitle = document.getElementById('admin-b-subtitle').value;

            if (title) document.getElementById('banner-title-text').innerText = title;
            if (subtitle) document.getElementById('banner-subtitle-text').innerText = subtitle;
            alert('Banner-ը հաջողությամբ թարմացվեց');
        }

        function renderProducts() {
            const container = document.getElementById('products-grid-container');
            const adminList = document.getElementById('admin-product-list');
            container.innerHTML = '';
            adminList.innerHTML = '';

            products.forEach(p => {
                container.innerHTML += `
                    <div class="product-card">
                        <div class="img-container">
                            <img src="${p.img}" onerror="this.onerror=null;this.src='${FALLBACK_IMG}';">
                        </div>
                        <div class="product-info">
                            <div class="product-title">${p.title}</div>
                            <div style="font-weight: bold; color: #4a3525;">${p.price.toLocaleString()} ֏</div>
                            <div class="card-footer">
                                <span style="font-size: 10px; color: green;">Առկա է</span>
                                <button class="add-cart-btn" onclick="addToCart('${p.title}', ${p.price})">
                                    <i data-lucide="plus" size="16"></i>
                                </button>
                            </div>
                        </div>
                    </div>`;

                adminList.innerHTML += `
                    <div class="admin-item-row">
                        <div><strong>${p.title}</strong> - ${p.price.toLocaleString()} ֏</div>
                        <button class="btn-danger" onclick="adminDeleteProduct(${p.id})">Ջնջել</button>
                    </div>`;
            });
            lucide.createIcons();
        }

        function renderAdminUsers() {
            const usersContainer = document.getElementById('admin-users-list');
            document.getElementById('users-count').innerText = registeredUsersList.length;

            if (registeredUsersList.length === 0) {
                usersContainer.innerHTML = '<p style="color: #666; font-size: 13px;">Դեռ ոչ մի օգտատեր գրանցված չէ</p>';
                return;
            }

            let html = '';
            registeredUsersList.forEach((u, i) => {
                html += `
                    <div class="user-card-item">
                        <strong>#${i+1} 📧 ${u.email}</strong><br>
                        📱 ${u.phone}<br>
                        📍 ${u.address}
                    </div>`;
            });
            usersContainer.innerHTML = html;
        }

        function adminAddProduct() {
            const title = document.getElementById('admin-p-title').value;
            const price = parseFloat(document.getElementById('admin-p-price').value);
            const imgInput = document.getElementById('admin-p-img').value.trim();
            const img = imgInput ? imgInput : FALLBACK_IMG;

            if (title && price) {
                products.push({ id: Date.now(), title, price, img });
                renderProducts();
                document.getElementById('admin-p-title').value = '';
                document.getElementById('admin-p-price').value = '';
                document.getElementById('admin-p-img').value = '';
                alert('Ապրանքը ավելացվեց');
            }
        }

        function adminDeleteProduct(id) {
            products = products.filter(p => p.id !== id);
            renderProducts();
        }

        function switchPage(pageId, element) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('page-' + pageId).classList.add('active');
            element.classList.add('active');
        }

        function addToCart(title, price) {
            cart.push({ title, price });
            updateCart();
            alert('Ապրանքն ավելացվեց զամբյուղում');
        }

        function updateCart() {
            const badge = document.getElementById('cart-badge');
            if (cart.length > 0) {
                badge.innerText = cart.length;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }

            const cartContainer = document.getElementById('cart-items');
            const cartSummary = document.getElementById('cart-summary');

            if (cart.length === 0) {
                cartContainer.innerHTML = '<p style="color: #666; font-size: 14px;">Զամբյուղը դատարկ է</p>';
                cartSummary.style.display = 'none';
            } else {
                let html = '';
                let total = 0;
                cart.forEach((item) => {
                    total += item.price;
                    html += `<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px;">
                        <span>${item.title}</span>
                        <strong>${item.price.toLocaleString()} ֏</strong>
                    </div>`;
                });
                cartContainer.innerHTML = html;
                document.getElementById('total-price').innerText = total.toLocaleString() + ' ֏';
                cartSummary.style.display = 'block';
            }
        }

        function login() {
            const email = document.getElementById('email-input').value;
            const phone = document.getElementById('phone-input').value;
            const region = document.getElementById('region-select').value;
            const city = document.getElementById('city-select').value;
            const street = document.getElementById('street-input').value;

            if (email && phone && region && city && street) {
                const fullAddress = `${region}, ${city}, ${street}`;
                userData = { email, phone, address: fullAddress };
                registeredUsersList.push(userData);
                renderAdminUsers();

                document.getElementById('logged-email').innerText = email;
                document.getElementById('profile-phone-text').innerText = phone;
                document.getElementById('profile-address-text').innerText = fullAddress;
                document.getElementById('header-address-text').innerText = fullAddress;

                document.getElementById('auth-form-view').style.display = 'none';
                document.getElementById('user-profile-view').style.display = 'block';
            } else {
                alert('Խնդրում ենք լրացնել բոլոր դաշտերը');
            }
        }

        function logout() {
            userData = { email: '', phone: '', address: '' };
            document.getElementById('header-address-text').innerText = 'Ընտրեք հասցեն (Պրոֆիլից)';
            document.getElementById('auth-form-view').style.display = 'block';
            document.getElementById('user-profile-view').style.display = 'none';
        }

        function openPaymentModal() {
            if (!userData.email) {
                alert('Վճարում անելու համար խնդրում ենք նախ գրանցվել «Պրոֆիլ» բաժնում');
                switchPage('profile', document.querySelectorAll('.nav-item')[3]);
                return;
            }
            document.getElementById('pay-modal-address').innerText = userData.address;
            document.getElementById('pay-modal-phone').innerText = userData.phone;
            document.getElementById('payment-modal').style.display = 'flex';
        }

        function closePaymentModal() {
            document.getElementById('payment-modal').style.display = 'none';
        }

        function processPayment() {
            const cardNum = document.getElementById('card-number').value;
            if (!cardNum) {
                alert('Խնդրում ենք լրացնել բանկային քարտի տվյալները');
                return;
            }
            alert('Վճարումը հաջողությամբ կատարվեց: Պատվերը կառաքվի՝ ' + userData.address);
            cart = [];
            updateCart();
            closePaymentModal();
            switchPage('home', document.querySelectorAll('.nav-item')[0]);
        }

        renderProducts();
        renderAdminUsers();
    </script>
</body>
</html>
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

print("Սերվերը աշխատում է...")
webbrowser.open("http://localhost:8000")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    httpd.serve_forever()
