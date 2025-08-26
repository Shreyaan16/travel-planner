// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Utility Functions
class TravelBookingAPI {
    constructor() {
        this.token = localStorage.getItem('token');
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        if (this.token && !endpoint.includes('/register') && !endpoint.includes('/token')) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }

    // Authentication methods
    async login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/token`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }

        this.token = data.access_token;
        localStorage.setItem('token', this.token);
        return data;
    }

    async register(userData) {
        return await this.request('/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async getCurrentUser() {
        return await this.request('/users/me');
    }

    async updateProfile(userData) {
        return await this.request('/users/me', {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    }

    // Travel options methods
    async getTravelOptions(filters = {}) {
        const params = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) params.append(key, value);
        });
        
        const queryString = params.toString();
        const endpoint = queryString ? `/travel-options?${queryString}` : '/travel-options';
        
        return await this.request(endpoint);
    }

    async getTravelOption(optionId) {
        return await this.request(`/travel-options/${optionId}`);
    }

    // Booking methods
    async createBooking(bookingData) {
        return await this.request('/bookings', {
            method: 'POST',
            body: JSON.stringify(bookingData)
        });
    }

    async getUserBookings() {
        return await this.request('/bookings');
    }

    async getBooking(bookingId) {
        return await this.request(`/bookings/${bookingId}`);
    }

    async cancelBooking(bookingId) {
        return await this.request(`/bookings/${bookingId}/cancel`, {
            method: 'PUT'
        });
    }

    logout() {
        this.token = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    }

    isAuthenticated() {
        return !!this.token;
    }
}

// Global API instance
const api = new TravelBookingAPI();

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showLoading(show = true) {
    const loadingDiv = document.querySelector('.loading');
    if (loadingDiv) {
        loadingDiv.style.display = show ? 'block' : 'none';
    }
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatPrice(price) {
    return `₹${parseFloat(price).toLocaleString('en-IN')}`;
}

// Navigation functions
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });
    
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.remove('hidden');
    }
}

function updateNavigation() {
    const isAuth = api.isAuthenticated();
    const authLinks = document.querySelectorAll('.auth-required');
    const guestLinks = document.querySelectorAll('.guest-only');
    
    authLinks.forEach(link => {
        link.style.display = isAuth ? 'block' : 'none';
    });
    
    guestLinks.forEach(link => {
        link.style.display = isAuth ? 'none' : 'block';
    });

    if (isAuth) {
        loadUserInfo();
    }
}

async function loadUserInfo() {
    try {
        const user = await api.getCurrentUser();
        localStorage.setItem('user', JSON.stringify(user));
        
        const userNameElement = document.getElementById('userName');
        if (userNameElement) {
            userNameElement.textContent = user.full_name || user.username;
        }
    } catch (error) {
        console.error('Failed to load user info:', error);
        api.logout();
        updateNavigation();
        showSection('login-section');
    }
}

// Authentication functions
async function handleLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const username = formData.get('username');
    const password = formData.get('password');

    try {
        showLoading(true);
        await api.login(username, password);
        showAlert('Login successful!', 'success');
        updateNavigation();
        showSection('home-section');
        loadTravelOptions();
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const userData = {
        username: formData.get('username'),
        email: formData.get('email'),
        password: formData.get('password'),
        full_name: formData.get('full_name'),
        phone_number: formData.get('phone_number')
    };

    const confirmPassword = formData.get('confirm_password');
    if (userData.password !== confirmPassword) {
        showAlert('Passwords do not match', 'error');
        return;
    }

    try {
        showLoading(true);
        await api.register(userData);
        showAlert('Registration successful! Please login.', 'success');
        showSection('login-section');
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function handleLogout() {
    api.logout();
    updateNavigation();
    showSection('login-section');
    showAlert('Logged out successfully', 'info');
}

// Travel options functions
async function loadTravelOptions(filters = {}) {
    try {
        showLoading(true);
        const options = await api.getTravelOptions(filters);
        displayTravelOptions(options);
    } catch (error) {
        showAlert('Failed to load travel options', 'error');
    } finally {
        showLoading(false);
    }
}

function displayTravelOptions(options) {
    const container = document.getElementById('travelOptionsContainer');
    
    if (options.length === 0) {
        container.innerHTML = '<p>No travel options found matching your criteria.</p>';
        return;
    }

    container.innerHTML = options.map(option => `
        <div class="travel-card">
            <div class="travel-header">
                <span class="travel-type">${option.type}</span>
                <span class="travel-price">${formatPrice(option.price_per_seat)}</span>
            </div>
            <div class="travel-route">${option.source} → ${option.destination}</div>
            <h3>${option.title}</h3>
            <div class="travel-details">
                <div class="detail-item">
                    <div class="detail-label">Departure</div>
                    <div class="detail-value">${formatDateTime(option.departure_time)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Arrival</div>
                    <div class="detail-value">${formatDateTime(option.arrival_time)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Available Seats</div>
                    <div class="detail-value seats-available">${option.available_seats}</div>
                </div>
            </div>
            <button class="btn" onclick="openBookingModal(${option.option_id})">Book Now</button>
        </div>
    `).join('');
}

async function handleSearch(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const filters = {
        type: formData.get('type'),
        source: formData.get('source'),
        destination: formData.get('destination'),
        date: formData.get('date'),
        min_price: formData.get('min_price'),
        max_price: formData.get('max_price')
    };

    // Remove empty filters
    Object.keys(filters).forEach(key => {
        if (!filters[key]) delete filters[key];
    });

    await loadTravelOptions(filters);
}

// Booking functions
async function openBookingModal(optionId) {
    try {
        const option = await api.getTravelOption(optionId);
        
        document.getElementById('bookingOptionId').value = option.option_id;
        document.getElementById('bookingTitle').textContent = option.title;
        document.getElementById('bookingRoute').textContent = `${option.source} → ${option.destination}`;
        document.getElementById('bookingPrice').textContent = formatPrice(option.price_per_seat);
        document.getElementById('bookingAvailableSeats').textContent = option.available_seats;
        
        const seatsInput = document.getElementById('numSeats');
        seatsInput.max = option.available_seats;
        seatsInput.value = 1;
        
        updateTotalPrice();
        
        document.getElementById('bookingModal').classList.add('active');
    } catch (error) {
        showAlert('Failed to load booking details', 'error');
    }
}

function closeBookingModal() {
    document.getElementById('bookingModal').classList.remove('active');
}

function updateTotalPrice() {
    const priceText = document.getElementById('bookingPrice').textContent;
    const price = parseFloat(priceText.replace('₹', '').replace(',', ''));
    const seats = parseInt(document.getElementById('numSeats').value) || 1;
    const total = price * seats;
    
    document.getElementById('totalPrice').textContent = formatPrice(total);
}

async function handleBooking(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const bookingData = {
        option_id: parseInt(formData.get('option_id')),
        num_seats: parseInt(formData.get('num_seats'))
    };

    try {
        showLoading(true);
        await api.createBooking(bookingData);
        showAlert('Booking created successfully!', 'success');
        closeBookingModal();
        loadTravelOptions(); // Refresh to show updated seat counts
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Bookings management
async function loadUserBookings() {
    try {
        showLoading(true);
        const bookings = await api.getUserBookings();
        displayUserBookings(bookings);
    } catch (error) {
        showAlert('Failed to load bookings', 'error');
    } finally {
        showLoading(false);
    }
}

function displayUserBookings(bookings) {
    const container = document.getElementById('bookingsContainer');
    
    if (bookings.length === 0) {
        container.innerHTML = '<p>You have no bookings yet.</p>';
        return;
    }

    container.innerHTML = bookings.map(booking => `
        <div class="booking-card">
            <div class="booking-header">
                <span class="booking-id">Booking #${booking.booking_id}</span>
                <span class="booking-status status-${booking.status.toLowerCase()}">${booking.status}</span>
            </div>
            <div class="travel-route">${booking.travel_option.source} → ${booking.travel_option.destination}</div>
            <h3>${booking.travel_option.title}</h3>
            <div class="travel-details">
                <div class="detail-item">
                    <div class="detail-label">Departure</div>
                    <div class="detail-value">${formatDateTime(booking.travel_option.departure_time)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Seats</div>
                    <div class="detail-value">${booking.num_seats}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Total Price</div>
                    <div class="detail-value">${formatPrice(booking.total_price)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Booking Date</div>
                    <div class="detail-value">${formatDateTime(booking.booking_date)}</div>
                </div>
            </div>
            ${booking.status === 'Confirmed' ? 
                `<button class="btn btn-danger btn-small" onclick="cancelBooking(${booking.booking_id})">Cancel Booking</button>` : 
                ''
            }
        </div>
    `).join('');
}

async function cancelBooking(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking?')) {
        return;
    }

    try {
        showLoading(true);
        await api.cancelBooking(bookingId);
        showAlert('Booking cancelled successfully', 'success');
        loadUserBookings(); // Refresh the bookings list
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    updateNavigation();
    
    if (api.isAuthenticated()) {
        showSection('home-section');
        loadTravelOptions();
    } else {
        showSection('login-section');
    }

    // Event listeners
    document.getElementById('loginForm')?.addEventListener('submit', handleLogin);
    document.getElementById('registerForm')?.addEventListener('submit', handleRegister);
    document.getElementById('searchForm')?.addEventListener('submit', handleSearch);
    document.getElementById('bookingForm')?.addEventListener('submit', handleBooking);
    
    // Number input listener for total price calculation
    document.getElementById('numSeats')?.addEventListener('input', updateTotalPrice);

    // Modal close listeners
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('booking-modal')) {
            closeBookingModal();
        }
    });
});
