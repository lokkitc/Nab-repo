(function() {
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    function handleAddToCart(productId, quantity) {
        console.log('Attempting to add product:', productId, 'quantity:', quantity);
        
        fetch("{% url 'product:add_to_cart' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                'product_id': productId,
                'quantity': quantity
            })
        })
        .then(response => {
            if (!response.ok) {
                console.error('Server response:', response.status, response.statusText);
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Товар добавлен в корзину!');
                // Обновляем максимальное доступное количество
                const quantityInput = document.getElementById('quantity');
                quantityInput.max = data.remaining_stock;
                if (data.remaining_stock === 0) {
                    const addToCartBtn = document.querySelector('.btn-add-cart');
                    addToCartBtn.disabled = true;
                    addToCartBtn.textContent = 'Нет в наличии';
                }
            } else {
                alert(data.error || 'Произошла ошибка при добавлении товара');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Произошла ошибка при добавлении товара в корзину');
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        const quantityInput = document.getElementById('quantity');
        const minusBtn = document.querySelector('.quantity-btn.minus');
        const plusBtn = document.querySelector('.quantity-btn.plus');
        const addToCartBtn = document.querySelector('.btn-add-cart');

        // Обработчики кнопок +/-
        minusBtn.addEventListener('click', () => {
            let value = parseInt(quantityInput.value);
            if (value > 1) {
                quantityInput.value = value - 1;
            }
        });

        plusBtn.addEventListener('click', () => {
            let value = parseInt(quantityInput.value);
            let max = parseInt(quantityInput.max);
            if (value < max) {
                quantityInput.value = value + 1;
            }
        });

        // Валидация ввода
        quantityInput.addEventListener('change', () => {
            let value = parseInt(quantityInput.value);
            let max = parseInt(quantityInput.max);
            let min = parseInt(quantityInput.min);

            if (value > max) {
                quantityInput.value = max;
                alert(`Максимальное доступное количество: ${max}`);
            }
            if (value < min) {
                quantityInput.value = min;
            }
        });

        // Обработчик добавления в корзину
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', function() {
                const productId = this.getAttribute('data-product-id');
                const quantity = parseInt(quantityInput.value);
                handleAddToCart(productId, quantity);
            });
        }
    });
})();