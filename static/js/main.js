document.addEventListener('DOMContentLoaded', function() {
    // Initialize price range sliders
    const minPriceSlider = document.getElementById('minPrice');
    const maxPriceSlider = document.getElementById('maxPrice');
    const minPriceValue = document.getElementById('minPriceValue');
    const maxPriceValue = document.getElementById('maxPriceValue');

    // Update price range display
    function updatePriceRange() {
        minPriceValue.textContent = minPriceSlider.value;
        maxPriceValue.textContent = maxPriceSlider.value;
    }

    minPriceSlider.addEventListener('input', updatePriceRange);
    maxPriceSlider.addEventListener('input', updatePriceRange);

    // Function to fetch and display products
    async function fetchProducts() {
        const categories = Array.from(document.querySelectorAll('.category-filter:checked'))
            .map(checkbox => checkbox.value);
        
        const params = new URLSearchParams({
            min_price: minPriceSlider.value,
            max_price: maxPriceSlider.value,
            min_rating: document.getElementById('ratingFilter').value,
            discount: document.getElementById('discountFilter').value,
            category: categories.join(',')
        });

        try {
            const response = await fetch(`/api/products?${params}`);
            const products = await response.json();
            displayProducts(products);
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    }

    // Function to display products
    function displayProducts(products) {
        const container = document.getElementById('productsContainer');
        container.innerHTML = '';

        products.forEach(product => {
            const productCard = `
                <div class="col-md-4">
                    <div class="card product-card">
                        ${product.discount > 0 ? `<div class="discount-badge">${product.discount}% OFF</div>` : ''}
                        <img src="${product.image_url}" class="card-img-top product-image" alt="${product.name}">
                        <div class="card-body">
                            <h5 class="card-title">${product.name}</h5>
                            <p class="card-text">${product.description}</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="price">
                                    ${product.discount > 0 ? 
                                        `<span class="text-muted text-decoration-line-through">$${product.price.toFixed(2)}</span>
                                         <span class="text-danger">$${(product.price * (1 - product.discount/100)).toFixed(2)}</span>` :
                                        `<span>$${product.price.toFixed(2)}</span>`
                                    }
                                </div>
                                <div class="rating">
                                    ${'★'.repeat(Math.floor(product.rating))}${product.rating % 1 >= 0.5 ? '½' : ''}
                                    ${'☆'.repeat(5 - Math.ceil(product.rating))}
                                </div>
                            </div>
                            <button class="btn btn-primary w-100 mt-2">Add to Cart</button>
                        </div>
                    </div>
                </div>
            `;
            container.innerHTML += productCard;
        });
    }

    // Apply filters button click handler
    document.getElementById('applyFilters').addEventListener('click', fetchProducts);

    // Initial load of products
    fetchProducts();
});
