const openPopupButton = document.getElementById('open_popup');
const popup = document.getElementById('popup');
const closePopupButton = document.getElementById('close_popup');

// Função para abrir o pop-up
openPopupButton.addEventListener('click', () => {
    popup.style.display = 'flex';
});

// Função para fechar o pop-up
closePopupButton.addEventListener('click', () => {
    popup.style.display = 'none';
});

// Fecha o pop-up se o usuário clicar fora do conteúdo
window.addEventListener('click', (event) => {
    if (event.target === popup) {
        popup.style.display = 'none';
    }
});