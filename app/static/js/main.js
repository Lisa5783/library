// Глобальное состояние приложения
let books = [];
let branches = [];
let faculties = [];
let currentBookId = null;
let currentBranchId = null;

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Инициализация тестовых данных
    initializeTestData();
    
    // Настройка навигации
    setupNavigation();
    
    // Обновление интерфейса
    updateDashboard();
    updateBooksTable();
    updateBranchesGrid();
    updateReportSelects();
    
    // Настройка поиска
    setupSearch();
    
    console.log('Приложение инициализировано');
    showNotification('Система управления библиотекой готова к работе', 'success');
}

// Инициализация тестовых данных
function initializeTestData() {
    // Филиалы
    branches = [
        { id: 1, name: "Центральный филиал", location: "ул. Пушкина, д. 1" },
        { id: 2, name: "Технический филиал", location: "пр. Науки, д. 15" },
        { id: 3, name: "Гуманитарный филиал", location: "ул. Литературная, д. 8" }
    ];

    // Факультеты
    faculties = [
        { id: 1, name: "Информационные технологии" },
        { id: 2, name: "Математика и физика" },
        { id: 3, name: "История и филология" },
        { id: 4, name: "Инженерное дело" }
    ];

    // Книги
    books = [
        {
            id: 1,
            title: "Основы программирования",
            authors: "Иван Иванов, Петр Петров",
            publisher: "Техническая литература",
            year: 2023,
            pages: 450,
            illustrations: 120,
            cost: 1500.0,
            branch_id: 2,
            copies_available: 5,
            times_issued: 23,
            faculties: [1, 4]
        },
        {
            id: 2,
            title: "Математический анализ",
            authors: "Анна Смирнова",
            publisher: "Университетское издательство",
            year: 2022,
            pages: 680,
            illustrations: 85,
            cost: 2200.0,
            branch_id: 1,
            copies_available: 3,
            times_issued: 45,
            faculties: [2]
        },
        {
            id: 3,
            title: "История России",
            authors: "Сергей Николаев",
            publisher: "Историческое общество",
            year: 2021,
            pages: 520,
            illustrations: 200,
            cost: 1800.0,
            branch_id: 3,
            copies_available: 7,
            times_issued: 67,
            faculties: [3]
        }
    ];
}

// Настройка навигации
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = this.getAttribute('data-section');
            console.log('Навигация к разделу:', targetSection);
            
            if (targetSection) {
                showSection(targetSection);
                
                // Обновление активной кнопки
                navButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
    
    console.log('Навигация настроена, найдено кнопок:', navButtons.length);
}

function showSection(sectionId) {
    console.log('Показываем раздел:', sectionId);
    
    // Скрываем все секции
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
        section.style.display = 'none';
    });
    
    // Показываем нужную секцию
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        targetSection.style.display = 'block';
        console.log('Раздел', sectionId, 'активирован');
    } else {
        console.error('Раздел не найден:', sectionId);
    }
}

// Обновление дашборда
function updateDashboard() {
    const totalBooksEl = document.getElementById('total-books');
    const totalBranchesEl = document.getElementById('total-branches');
    const totalFacultiesEl = document.getElementById('total-faculties');
    const totalCopiesEl = document.getElementById('total-copies');
    
    if (totalBooksEl) totalBooksEl.textContent = books.length;
    if (totalBranchesEl) totalBranchesEl.textContent = branches.length;
    if (totalFacultiesEl) totalFacultiesEl.textContent = faculties.length;
    if (totalCopiesEl) totalCopiesEl.textContent = books.reduce((sum, book) => sum + book.copies_available, 0);
    
    updateRecentBooks();
}

function updateRecentBooks() {
    const container = document.getElementById('recent-books-list');
    if (!container) return;
    
    const recentBooks = [...books].sort((a, b) => b.id - a.id).slice(0, 5);
    
    if (recentBooks.length === 0) {
        container.innerHTML = '<p class="text-secondary">Нет добавленных книг</p>';
        return;
    }
    
    container.innerHTML = recentBooks.map(book => {
        const branch = branches.find(b => b.id === book.branch_id);
        return `
            <div class="book-item">
                <div class="book-info">
                    <h4 class="book-title">${book.title}</h4>
                    <p class="book-details">${book.authors} • ${book.publisher} • ${book.year} • ${branch ? branch.name : 'Неизвестный филиал'}</p>
                </div>
            </div>
        `;
    }).join('');
}

// Управление книгами
function updateBooksTable() {
    const tbody = document.getElementById('books-table-body');
    if (!tbody) return;
    
    if (books.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem;">Книг не найдено</td></tr>';
        return;
    }
    
    tbody.innerHTML = books.map(book => {
        const branch = branches.find(b => b.id === book.branch_id);
        return `
            <tr>
                <td><strong>${book.title}</strong></td>
                <td>${book.authors}</td>
                <td>${book.publisher}</td>
                <td>${book.year}</td>
                <td>${branch ? branch.name : 'Неизвестный филиал'}</td>
                <td>${book.copies_available}</td>
                <td>
                    <div class="table-actions">
                        <button class="btn-table btn-edit" onclick="editBook(${book.id})">✏️</button>
                        <button class="btn-table btn-delete" onclick="deleteBook(${book.id})">🗑️</button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

function showBookModal(bookId = null) {
    const modal = document.getElementById('book-modal');
    const title = document.getElementById('book-modal-title');
    const branchSelect = document.getElementById('book-branch');
    
    if (!modal || !title || !branchSelect) {
        console.error('Элементы модального окна не найдены');
        return;
    }
    
    // Заполнение списка филиалов
    branchSelect.innerHTML = '<option value="">Выберите филиал</option>' +
        branches.map(branch => `<option value="${branch.id}">${branch.name}</option>`).join('');
    
    if (bookId) {
        const book = books.find(b => b.id === bookId);
        if (book) {
            title.textContent = 'Редактировать книгу';
            currentBookId = bookId;
            
            // Заполнение формы
            document.getElementById('book-title').value = book.title || '';
            document.getElementById('book-authors').value = book.authors || '';
            document.getElementById('book-publisher').value = book.publisher || '';
            document.getElementById('book-year').value = book.year || '';
            document.getElementById('book-pages').value = book.pages || '';
            document.getElementById('book-illustrations').value = book.illustrations || 0;
            document.getElementById('book-cost').value = book.cost || '';
            document.getElementById('book-branch').value = book.branch_id || '';
            document.getElementById('book-copies').value = book.copies_available || '';
            document.getElementById('book-times-issued').value = book.times_issued || 0;
            
            // Факультеты
            if (book.faculties && Array.isArray(book.faculties)) {
                const bookFaculties = book.faculties.map(id => faculties.find(f => f.id === id)?.name).filter(Boolean);
                document.getElementById('book-faculties').value = bookFaculties.join(', ');
            }
        }
    } else {
        title.textContent = 'Добавить книгу';
        currentBookId = null;
        const form = document.getElementById('book-form');
        if (form) form.reset();
    }
    
    modal.classList.remove('hidden');
    modal.classList.add('show');
}

function hideBookModal() {
    const modal = document.getElementById('book-modal');
    if (!modal) return;
    
    modal.classList.remove('show');
    modal.classList.add('hidden');
    currentBookId = null;
}

function saveBook() {
    const form = document.getElementById('book-form');
    if (!form || !form.checkValidity()) {
        if (form) form.reportValidity();
        return;
    }
    
    const bookData = {
        title: document.getElementById('book-title').value,
        authors: document.getElementById('book-authors').value,
        publisher: document.getElementById('book-publisher').value,
        year: parseInt(document.getElementById('book-year').value),
        pages: parseInt(document.getElementById('book-pages').value),
        illustrations: parseInt(document.getElementById('book-illustrations').value) || 0,
        cost: parseFloat(document.getElementById('book-cost').value),
        branch_id: parseInt(document.getElementById('book-branch').value),
        copies_available: parseInt(document.getElementById('book-copies').value),
        times_issued: parseInt(document.getElementById('book-times-issued').value) || 0,
        faculties: []
    };
    
    // Обработка факультетов
    const facultiesInput = document.getElementById('book-faculties').value;
    if (facultiesInput && facultiesInput.trim()) {
        const facultyNames = facultiesInput.split(',').map(s => s.trim());
        bookData.faculties = facultyNames.map(name => {
            let faculty = faculties.find(f => f.name === name);
            if (!faculty) {
                // Создаем новый факультет
                const newId = Math.max(...faculties.map(f => f.id), 0) + 1;
                faculty = { id: newId, name: name };
                faculties.push(faculty);
            }
            return faculty.id;
        });
    }
    
    try {
        if (currentBookId) {
            // Редактирование
            const bookIndex = books.findIndex(b => b.id === currentBookId);
            if (bookIndex !== -1) {
                books[bookIndex] = { ...books[bookIndex], ...bookData };
                showNotification('Книга успешно обновлена', 'success');
            }
        } else {
            // Добавление
            const newId = Math.max(...books.map(b => b.id), 0) + 1;
            books.push({ id: newId, ...bookData });
            showNotification('Книга успешно добавлена', 'success');
        }
        
        updateBooksTable();
        updateDashboard();
        updateReportSelects();
        hideBookModal();
    } catch (error) {
        console.error('Ошибка при сохранении книги:', error);
        showNotification('Ошибка при сохранении книги', 'error');
    }
}

function editBook(bookId) {
    showBookModal(bookId);
}

function deleteBook(bookId) {
    const book = books.find(b => b.id === bookId);
    if (!book) return;
    
    if (confirm(`Вы уверены, что хотите удалить книгу "${book.title}"?`)) {
        try {
            books = books.filter(b => b.id !== bookId);
            updateBooksTable();
            updateDashboard();
            updateReportSelects();
            showNotification('Книга успешно удалена', 'success');
        } catch (error) {
            console.error('Ошибка при удалении книги:', error);
            showNotification('Ошибка при удалении книги', 'error');
        }
    }
}

// Управление филиалами
function updateBranchesGrid() {
    const grid = document.getElementById('branches-grid');
    if (!grid) return;
    
    if (branches.length === 0) {
        grid.innerHTML = '<p class="text-secondary">Филиалов не найдено</p>';
        return;
    }
    
    grid.innerHTML = branches.map(branch => {
        const branchBooks = books.filter(b => b.branch_id === branch.id);
        const totalCopies = branchBooks.reduce((sum, book) => sum + book.copies_available, 0);
        
        return `
            <div class="branch-card">
                <div class="branch-header">
                    <h3 class="branch-name">${branch.name}</h3>
                    <div class="branch-actions">
                        <button class="btn-table btn-edit" onclick="editBranch(${branch.id})">✏️</button>
                        <button class="btn-table btn-delete" onclick="deleteBranch(${branch.id})">🗑️</button>
                    </div>
                </div>
                <p class="branch-location">📍 ${branch.location}</p>
                <div class="branch-stats">
                    <div class="branch-stat">
                        <div class="branch-stat-number">${branchBooks.length}</div>
                        <div class="branch-stat-label">Книг</div>
                    </div>
                    <div class="branch-stat">
                        <div class="branch-stat-number">${totalCopies}</div>
                        <div class="branch-stat-label">Экземпляров</div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function showBranchModal(branchId = null) {
    const modal = document.getElementById('branch-modal');
    const title = document.getElementById('branch-modal-title');
    
    if (!modal || !title) return;
    
    if (branchId) {
        const branch = branches.find(b => b.id === branchId);
        if (branch) {
            title.textContent = 'Редактировать филиал';
            currentBranchId = branchId;
            document.getElementById('branch-name').value = branch.name || '';
            document.getElementById('branch-location').value = branch.location || '';
        }
    } else {
        title.textContent = 'Добавить филиал';
        currentBranchId = null;
        const form = document.getElementById('branch-form');
        if (form) form.reset();
    }
    
    modal.classList.remove('hidden');
    modal.classList.add('show');
}

function hideBranchModal() {
    const modal = document.getElementById('branch-modal');
    if (!modal) return;
    
    modal.classList.remove('show');
    modal.classList.add('hidden');
    currentBranchId = null;
}

function saveBranch() {
    const form = document.getElementById('branch-form');
    if (!form || !form.checkValidity()) {
        if (form) form.reportValidity();
        return;
    }
    
    const branchData = {
        name: document.getElementById('branch-name').value,
        location: document.getElementById('branch-location').value
    };
    
    try {
        if (currentBranchId) {
            // Редактирование
            const branchIndex = branches.findIndex(b => b.id === currentBranchId);
            if (branchIndex !== -1) {
                branches[branchIndex] = { ...branches[branchIndex], ...branchData };
                showNotification('Филиал успешно обновлен', 'success');
            }
        } else {
            // Добавление
            const newId = Math.max(...branches.map(b => b.id), 0) + 1;
            branches.push({ id: newId, ...branchData });
            showNotification('Филиал успешно добавлен', 'success');
        }
        
        updateBranchesGrid();
        updateDashboard();
        updateReportSelects();
        hideBranchModal();
    } catch (error) {
        console.error('Ошибка при сохранении филиала:', error);
        showNotification('Ошибка при сохранении филиала', 'error');
    }
}

function editBranch(branchId) {
    showBranchModal(branchId);
}

function deleteBranch(branchId) {
    const branch = branches.find(b => b.id === branchId);
    if (!branch) return;
    
    // Проверяем, есть ли книги в этом филиале
    const booksInBranch = books.filter(b => b.branch_id === branchId);
    if (booksInBranch.length > 0) {
        showNotification(`Нельзя удалить филиал "${branch.name}" - в нем есть книги`, 'error');
        return;
    }
    
    if (confirm(`Вы уверены, что хотите удалить филиал "${branch.name}"?`)) {
        try {
            branches = branches.filter(b => b.id !== branchId);
            updateBranchesGrid();
            updateDashboard();
            updateReportSelects();
            showNotification('Филиал успешно удален', 'success');
        } catch (error) {
            console.error('Ошибка при удалении филиала:', error);
            showNotification('Ошибка при удалении филиала', 'error');
        }
    }
}

// Отчеты
function updateReportSelects() {
    // Обновление списков для отчетов
    const bookSelects = ['report1-book', 'report2-book'];
    const branchSelects = ['report1-branch', 'report2-branch'];
    
    bookSelects.forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = '<option value="">Выберите книгу</option>' +
                books.map(book => `<option value="${book.id}">${book.title}</option>`).join('');
        }
    });
    
    branchSelects.forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = '<option value="">Выберите филиал</option>' +
                branches.map(branch => `<option value="${branch.id}">${branch.name}</option>`).join('');
        }
    });
}

function generateReport1() {
    const bookId = document.getElementById('report1-book').value;
    const branchId = document.getElementById('report1-branch').value;
    const resultDiv = document.getElementById('report1-result');
    
    if (!resultDiv) return;
    
    if (!bookId || !branchId) {
        resultDiv.innerHTML = '<p style="color: var(--color-error);">Выберите книгу и филиал</p>';
        return;
    }
    
    const book = books.find(b => b.id == bookId);
    const branch = branches.find(b => b.id == branchId);
    
    if (!book || !branch) {
        resultDiv.innerHTML = '<p style="color: var(--color-error);">Книга или филиал не найдены</p>';
        return;
    }
    
    let copies = 0;
    if (book.branch_id == branchId) {
        copies = book.copies_available;
    }
    
    resultDiv.className = 'report-result success';
    resultDiv.innerHTML = `
        <h4>Результат:</h4>
        <p>В филиале "<strong>${branch.name}</strong>" находится <strong>${copies}</strong> экземпляров книги "<strong>${book.title}</strong>"</p>
    `;
}

function generateReport2() {
    const bookId = document.getElementById('report2-book').value;
    const branchId = document.getElementById('report2-branch').value;
    const resultDiv = document.getElementById('report2-result');
    
    if (!resultDiv) return;
    
    if (!bookId || !branchId) {
        resultDiv.innerHTML = '<p style="color: var(--color-error);">Выберите книгу и филиал</p>';
        return;
    }
    
    const book = books.find(b => b.id == bookId);
    const branch = branches.find(b => b.id == branchId);
    
    if (!book || !branch) {
        resultDiv.innerHTML = '<p style="color: var(--color-error);">Книга или филиал не найдены</p>';
        return;
    }
    
    let bookFaculties = [];
    if (book.branch_id == branchId && book.faculties) {
        bookFaculties = book.faculties.map(id => faculties.find(f => f.id === id)).filter(Boolean);
    }
    
    resultDiv.className = 'report-result success';
    if (bookFaculties.length > 0) {
        resultDiv.innerHTML = `
            <h4>Результат:</h4>
            <p>Книга "<strong>${book.title}</strong>" используется на <strong>${bookFaculties.length}</strong> факультете(ах) в филиале "<strong>${branch.name}</strong>":</p>
            <ul>
                ${bookFaculties.map(faculty => `<li>${faculty.name}</li>`).join('')}
            </ul>
        `;
    } else {
        resultDiv.innerHTML = `
            <h4>Результат:</h4>
            <p>Книга "<strong>${book.title}</strong>" не используется ни на одном факультете в филиале "<strong>${branch.name}</strong>" или отсутствует в данном филиале</p>
        `;
    }
}

// Поиск
function setupSearch() {
    const searchInput = document.getElementById('books-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            filterBooks(query);
        });
    }
}

function filterBooks(query) {
    const tbody = document.getElementById('books-table-body');
    if (!tbody) return;
    
    if (!query.trim()) {
        updateBooksTable();
        return;
    }
    
    const filteredBooks = books.filter(book => 
        book.title.toLowerCase().includes(query) ||
        book.authors.toLowerCase().includes(query) ||
        book.publisher.toLowerCase().includes(query)
    );
    
    if (filteredBooks.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem;">Книг не найдено</td></tr>';
        return;
    }
    
    tbody.innerHTML = filteredBooks.map(book => {
        const branch = branches.find(b => b.id === book.branch_id);
        return `
            <tr>
                <td><strong>${book.title}</strong></td>
                <td>${book.authors}</td>
                <td>${book.publisher}</td>
                <td>${book.year}</td>
                <td>${branch ? branch.name : 'Неизвестный филиал'}</td>
                <td>${book.copies_available}</td>
                <td>
                    <div class="table-actions">
                        <button class="btn-table btn-edit" onclick="editBook(${book.id})">✏️</button>
                        <button class="btn-table btn-delete" onclick="deleteBook(${book.id})">🗑️</button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// Система уведомлений
function showNotification(message, type = 'info') {
    const container = document.getElementById('notifications');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    container.appendChild(notification);
    
    // Показываем уведомление
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Скрываем через 4 секунды
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
    
    // Клик для закрытия
    notification.addEventListener('click', function() {
        this.classList.remove('show');
        setTimeout(() => {
            if (this.parentNode) {
                this.parentNode.removeChild(this);
            }
        }, 300);
    });
}

// Закрытие модальных окон при клике вне их
document.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal.show');
    modals.forEach(modal => {
        if (event.target === modal) {
            if (modal.id === 'book-modal') {
                hideBookModal();
            } else if (modal.id === 'branch-modal') {
                hideBranchModal();
            }
        }
    });
});

// Обработка ESC для закрытия модальных окон
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const activeModal = document.querySelector('.modal.show');
        if (activeModal) {
            if (activeModal.id === 'book-modal') {
                hideBookModal();
            } else if (activeModal.id === 'branch-modal') {
                hideBranchModal();
            }
        }
    }
});

// Обработка исключительных ситуаций
class BookNotFoundError extends Error {
    constructor(message) {
        super(message);
        this.name = 'BookNotFoundError';
    }
}

class BranchNotFoundError extends Error {
    constructor(message) {
        super(message);
        this.name = 'BranchNotFoundError';
    }
}

// Глобальный обработчик ошибок
window.addEventListener('error', function(event) {
    console.error('Произошла ошибка:', event.error);
    showNotification('Произошла непредвиденная ошибка', 'error');
});

// Хуки для логирования изменений (имитация SQLAlchemy событий)
function logChange(action, type, data) {
    const timestamp = new Date().toLocaleString('ru-RU');
    console.log(`[${timestamp}] ${action} ${type}:`, data);
}