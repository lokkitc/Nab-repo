document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profile-form');
    
    profileForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch('/user/update-profile/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Профиль успешно обновлен');
                location.reload();
            } else {
                alert('Ошибка при обновлении профиля: ' + JSON.stringify(data.errors));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Произошла ошибка при обновлении профиля');
        });
    });
}); 