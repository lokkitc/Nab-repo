document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.quantity-controls').forEach(control => {
        const minusBtn = control.querySelector('.quantity-btn:first-child');
        const plusBtn = control.querySelector('.quantity-btn:last-child');
        const quantitySpan = control.querySelector('.quantity');
        const itemId = control.closest('.product-card').dataset.itemId;

        minusBtn.addEventListener('click', () => updateQuantity(itemId, -1));
        plusBtn.addEventListener('click', () => updateQuantity(itemId, 1));
    });

    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', () => {
            const checkedItems = document.querySelectorAll('.product-checkbox:checked');
            checkedItems.forEach(checkbox => {
                const productCard = checkbox.closest('.product-card');
                const itemId = productCard.dataset.itemId;
                deleteItem(itemId);
            });
        });
    });

    async function updateQuantity(itemId, change) {
        const productCard = document.querySelector(`[data-item-id="${itemId}"]`);
        const quantitySpan = productCard.querySelector('.quantity');
        const currentQuantity = parseInt(quantitySpan.textContent);
        const newQuantity = currentQuantity + change;

        if (newQuantity < 1) return;

        try {
            const response = await fetch('/catalog/cart/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    item_id: itemId,
                    quantity: newQuantity
                })
            });

            const data = await response.json();
            if (data.success) {
                quantitySpan.textContent = data.quantity;
                updateTotals(data.cart_total);
            } else {
                alert(data.error);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function deleteItem(itemId) {
        try {
            const response = await fetch('/catalog/cart/delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    item_id: itemId
                })
            });

            const data = await response.json();
            if (data.success) {
                const productCard = document.querySelector(`[data-item-id="${itemId}"]`);
                productCard.remove();
                updateTotals(data.cart_total);
                updateItemsCount(data.items_count);
            } else {
                alert(data.error);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function updateTotals(cartTotal) {
        document.querySelector('.summary-row .bold').textContent = `${cartTotal} ₸`;
        document.querySelector('.summary-row.total span:last-child').textContent = `${cartTotal} ₸`;
    }

    function updateItemsCount(count) {
        document.querySelector('.btn-delete span').textContent = `Удалить (${count})`;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});